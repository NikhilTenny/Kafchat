import { AfterViewChecked, Component, ElementRef, OnInit, ViewChild } from '@angular/core';
import { Message, STATUSES } from './models';
import { USERS } from './data';
import { AuthService } from 'src/app/services/auth.service';
import { ChatUser } from 'src/app/components/chat/models';
import { catchError, Observable, throwError } from 'rxjs';

@Component({
  selector: 'app-chat',
  templateUrl: './chat.component.html',
  styleUrls: ['./chat.component.css']
})
export class ChatComponent implements OnInit, AfterViewChecked {
  statuses = STATUSES;
  activeUser: any;
  currentUser: any;
  users : ChatUser[] = [];
  expandStatuses = false;
  expanded = false;
  messageReceivedFrom = {
    img: 'https://cdn.livechat-files.com/api/file/lc/img/12385611/371bd45053f1a25d780d4908bde6b6ef',
    name: 'Media bot'
  }

  constructor(
        private apiService: AuthService
  ) {}

    @ViewChild('scrollMe') private myScrollContainer!: ElementRef;

    ngOnInit() { 
      
      this.get_users();
      this.get_current_user()
        this.scrollToBottom();
    }
        ngAfterViewChecked() {        
        this.scrollToBottom();        
    } 

  get_current_user() {
    this.currentUser = localStorage.getItem('userData');
    if (this.currentUser) {
      this.currentUser = JSON.parse(this.currentUser)
    } 

  }
  addNewMessage(inputField: any) {
    const val = inputField.value?.trim()
    if (val.length) {
      this.activeUser.messages.push({type: 'sent', body: val})
      console.log('activa: ', this.activeUser)

      let payload = {
        "receiver_id": this.activeUser.id,
        "conv_id": this.activeUser.conv_id,
        "body": val
      }

 
      this.apiService.sendMessage(payload).subscribe({
        error: (err) => console.error('Message send failed', err),
      });

      // this.activeUser.ws.send(
      //   JSON.stringify(
      //     {
      //       reciever_id: this.activeUser.id, 
      //       body: val, 
      //       conv_id: this.activeUser.conv_id
      //     })
      //   );
    }
    inputField.value = '';
  }

    scrollToBottom(): void {
        try {
            this.myScrollContainer.nativeElement.scrollTop = this.myScrollContainer.nativeElement.scrollHeight;
        } catch(err) { }                 
    }


    sendMessage(payload: any): Observable<any> {
      return this.apiService.sendMessage(payload).pipe(
        catchError(error => throwError(
          () => new Error('Failed to send message!')
        ))
      )
    }

    setUserActive(user: any) {
      this.activeUser = user;
      this.get_chat_history();
      this.connectToWS();
    }

    connectToWS() {
      if (this.activeUser.ws && this.activeUser.ws.readyState !== 1) {
        this.activeUser.ws = null;
        this.activeUser.status = STATUSES.OFFLINE;
      }
      if (this.activeUser.ws) {
        return;
      }
      const ws = new WebSocket(`ws://localhost:8000/ws/${this.activeUser.id}`);

      // const ws = new WebSocket('wss://compute.hotelway.ai:4443/?token=TESTTOKEN');
      this.activeUser.ws = ws;
      ws.onopen = (event) => this.onWSEvent(event, STATUSES.ONLINE);
      ws.onclose = (event) => this.onWSEvent(event, STATUSES.OFFLINE);
      ws.onerror = (event) => this.onWSEvent(event, STATUSES.OFFLINE);
      ws.onmessage = (result: any) => {
        const data = JSON.parse(result?.data || {});
        console.log('data got: ', data)

        data.type = 'replies'
        this.activeUser.messages.push(data)
          
       
      };
    }

    onWSEvent(event: any, status: STATUSES) {
      // this.users.forEach(u => u.ws === event.target ? u.status = status : null)
    }

    get_users() {
      /**
       * Handles the successful response from the API.
       * Maps each user to add a default profile image and status.
       * Sets the first user as active if users exist.
      */
      this.apiService.get_users().subscribe(
        {
          next: (response: ChatUser[]) => {
            this.users = response.map((user: ChatUser) => ({
              ...user,
              img: "https://images.pexels.com/photos/2613260/pexels-photo-2613260.jpeg?auto=compress&cs=tinysrgb&w=600",
              status: "busy"
            }));

            if (this.users.length > 0) {
              this.setUserActive(this.users[0]);
            }
          },
          error: (error: any) => {
            console.log('Error fetching users:', error);
          }
        }
      )
    }

    get_chat_history() {
      /**
       * Fetches chat history for the currently active user.
       * Updates conversation ID and categorizes messages based on sender.
      */
      this.apiService.get_chat_history(this.activeUser.user_name).subscribe({
        next: (response: any) => {
          this.activeUser['conv_id'] = response.conv_id
          let chat_history = response.chat_history    
          this.activeUser.messages = chat_history.map((msg:any) => ({
            ...msg,
            type: msg.sender_id === this.activeUser.id ? 'replies' : 'sent'
          }));
        },
    
        error: (error: any) => {
          console.error('Error fetching chat history:', error);
        }
      })




    }
}
// function heartbeat() {
//   clearTimeout(this.pingTimeout);

//   // Use `WebSocket#terminate()`, which immediately destroys the connection,
//   // instead of `WebSocket#close()`, which waits for the close timer.
//   // Delay should be equal to the interval at which your server
//   // sends out pings plus a conservative assumption of the latency.
//   this.pingTimeout = setTimeout(() => {
//     this.terminate();
//   }, 30000 + 1000);
// }



function ngOnInit() {
  throw new Error('Function not implemented.');
}

function ngAfterViewChecked() {
  throw new Error('Function not implemented.');
}

function addNewMessage(inputField: any) {
  throw new Error('Function not implemented.');
}

function scrollToBottom() {
  throw new Error('Function not implemented.');
}

function setUserActive(user: any) {
  throw new Error('Function not implemented.');
}

function connectToWS() {
  throw new Error('Function not implemented.');
}

function onWSEvent(event: Event | undefined, status: string, STATUSES: any) {
  throw new Error('Function not implemented.');
}

