import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { AuthService } from 'src/app/services/auth.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {
  loginForm!: FormGroup;

  constructor(
    private fb: FormBuilder,
    private router: Router,
    private apiService: AuthService,
  ) { }

  ngOnInit(): void {
    this.loginForm = this.fb.group({
      user_name: ['', [Validators.required,]],
      password: ['', Validators.required]
    });
  }

  onSubmit() {
    const { user_name, password } = this.loginForm.value;  // Get the form data

  
    this.apiService.login(user_name, password).subscribe(
      response => {
        localStorage.setItem('accessToken', response.access_token);  
        localStorage.setItem('userData', JSON.stringify(response.user_data));  
        this.router.navigate(['/chat']);  // Navigate to another page after successful login

      },
      error => {
        console.error('Login error:', error);
        // Handle error response, e.g., show an error message to the user
      }
    );

  }
  openRegistrationPage(){
    this.router.navigateByUrl("/sign-up");
  }

}
