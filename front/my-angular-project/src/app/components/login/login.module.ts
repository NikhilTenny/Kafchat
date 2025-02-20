// Angular Imports
import { NgModule } from '@angular/core';

// This Module's Components
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { LoginRoutingModule } from './login-routing.module'
import { CommonModule } from '@angular/common';
import { LoginComponent } from './login.component';

@NgModule({
    declarations: [LoginComponent],
    imports: [
        CommonModule,
        FormsModule,
        ReactiveFormsModule,
        LoginRoutingModule
    ]
})
export class LoginModule {

}