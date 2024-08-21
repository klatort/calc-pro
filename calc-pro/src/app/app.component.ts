import { Component } from '@angular/core';
import { MatIconModule } from '@angular/material/icon';
import { MatButtonModule } from '@angular/material/button';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatButton } from '@angular/material/button';
import { FileUploadService } from './file-upload.service';
import { HttpClientModule } from '@angular/common/http';
import { CommonModule } from '@angular/common';
import { MatTableModule } from '@angular/material/table';
import { MatCheckboxModule } from '@angular/material/checkbox';
import { FormsModule } from '@angular/forms';
import { Flavor } from './flavor';
import { MatSnackBar, MatSnackBarModule } from '@angular/material/snack-bar';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [
    MatToolbarModule,
    MatButtonModule,
    MatIconModule,
    MatButton,
    HttpClientModule,
    CommonModule,
    MatTableModule,
    MatCheckboxModule,
    MatSnackBarModule,
    FormsModule
  ],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css',
  providers: [FileUploadService,],
})
export class AppComponent {
  displayedColumns: string[] = ['name', 'windows'];
  flavors: Flavor[] = [];
  uploadedFile: string = '';

  constructor(private fileUploadService: FileUploadService, private snackBar: MatSnackBar) { }

  onFileChanged(event: any) {
    const selectedFile = event.target.files[0];
    if (selectedFile) {
      this.fileUploadService.uploadFile(selectedFile).subscribe(
        response => {
          console.log(response);
          this.flavors = response.map((item: any) => ({
            name: item.flavor,
            windows: false,
            row: item.row
          }));
          this.uploadedFile = `calc_${new Date().getTime()}.xlsx`;
          console.log('Upload success', this.flavors);
        },
        error => {
          this.snackBar.open('Upload error: ' + error.message, 'Close', {
            duration: 3000,
          });
        }
      );
    }
  }

  getCalc() {
    const payload = { 'flavors': this.flavors, 'uploadedFile': this.uploadedFile };
    this.fileUploadService.downloadCalc(payload).subscribe(
      blob => {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = this.uploadedFile;
        a.click();
        window.URL.revokeObjectURL(url);
      },
      error => {
        this.snackBar.open('Download error: ' + error, 'Close', {
          duration: 3000,
        });
      }
    );
  }

  isObject(value: any): boolean {
    return value !== null && typeof value === 'object';
  }
  logVal() {
    console.log(this.flavors);
  }
}
