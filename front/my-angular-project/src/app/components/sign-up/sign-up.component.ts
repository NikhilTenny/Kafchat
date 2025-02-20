import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { AuthService } from 'src/app/services/auth.service';


@Component({
  selector: 'app-sign-up',
  templateUrl: './sign-up.component.html',
  styleUrls: ['./sign-up.component.css']
})
export class SignUpComponent implements OnInit {

  constructor(
    private apiService: AuthService,
    private router: Router,
    private http: HttpClient
  ) { }

  ngOnInit(): void {
      // throw new Error('Method not implemented.');
  }

  onSubmit(form:any){

      if (form.invalid) {
        return;  // Prevent form submission if the form is invalid
      }
  
      const userData = form.value;  // Get the form data
  
      this.apiService.submitFormData(userData).subscribe(
        response => {
          console.log('User created successfully:', response);
          // Handle success response, e.g., show success message, navigate to login
        },
        error => {
          console.error('Error during sign-up:', error);
          // Handle error response, e.g., show error message
        }
      );
  
  }

  openLoginPage(){
      this.router.navigateByUrl("/login");
  }
}