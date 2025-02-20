// Angular Imports
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
// This Module's Components
import { SignUpComponent } from './sign-up.component';
import { SignUpRoutingModule } from './sign-up-routing.module';

@NgModule({
    declarations: [SignUpComponent],
    imports: [
        SignUpRoutingModule,
        FormsModule,
        CommonModule
    ]
})
export class SignUpModule {

}