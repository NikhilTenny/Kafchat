import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { ChatComponent } from './components/chat/chat.component';

const routes: Routes = [
  { path: 'login',loadChildren: () => import('./components/login/login.module').then(m => m.LoginModule)},
  { path: 'sign-up',loadChildren: () => import('./components/sign-up/sign-up.module').then(m => m.SignUpModule) },
  {path: 'chat', component: ChatComponent}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
