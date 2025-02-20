import { Routes } from '@angular/router';

export const routes: Routes = [
    { path: '/sign-up',loadChildren: () => import('./components/signup/signup.component').then(m => m.SignupComponent) }

];
