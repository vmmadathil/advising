import { Component } from '@angular/core';
import { LoginService } from './shared/repositories/login.service'; 

@Component({
  selector: 'my-app',
  templateUrl: './app.component.html',
  styleUrls: [ './app.component.css' ]
})
export class AppComponent  {
  name = 'Angular';
  public loggedIn = false;
  public users = [];

constructor(private ls: LoginService){

}

  login(loggedInTemp){
    this.loggedIn = loggedInTemp;
    this.getUsers();
  }

  getUsers(){
    this.ls.getUsers()
      .subscribe(resp => {
        this.users = resp.users;
      });
  }
}

