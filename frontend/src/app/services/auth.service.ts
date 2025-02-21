import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private apiUrl = 'http://localhost:8000/';
  constructor(private http: HttpClient) {
    
   }

   // Method to make a POST request
  submitFormData(formData: any): Observable<any> {
    let url = this.apiUrl + 'sign-up';
    return this.http.post(url, formData);
  }
  
  login(username: string, password: string): Observable<any> {
    let url = this.apiUrl + 'login';

    const body = new HttpParams()
      .set('client_id', "")
      .set('client_secret', "string")
      .set('scope', "string")
      .set('grant_type', "password")
      .set('username', username)
      .set('password', password);

    const headers = new HttpHeaders({
      'Content-Type': 'application/x-www-form-urlencoded'
    });

    return this.http.post(url, body, { headers });
  }

  get_users(): Observable<any> {
    const token = localStorage.getItem('accessToken'); // Retrieve token from localStorage

    const headers = new HttpHeaders({
      'Authorization': `Bearer ${token}` // Add token to the request
    });


    let url = this.apiUrl + 'users';
    return this.http.get(url, {headers});

  }

  get_chat_history(receiverUname: string): Observable<Object> {
    console.log('re: ', receiverUname)
    const token = localStorage.getItem('accessToken'); 
    const headers = new HttpHeaders({
      'Authorization': `Bearer ${token}` // Add token to the request
    });

    const params = new HttpParams().set('receiver_uname', receiverUname);

    let url = this.apiUrl + 'chat-history';
    return this.http.get(url, {headers, params});

  }

  sendMessage(payload: any) {
    console.log('payload: ', payload)
    const token = localStorage.getItem('accessToken'); 
    const headers = new HttpHeaders({
      'Authorization': `Bearer ${token}` // Add token to the request
    });


    let url = this.apiUrl + 'message';
    return this.http.post(url, payload, {headers});
  }

}
