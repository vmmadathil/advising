import { Component, OnInit, EventEmitter, Output } from '@angular/core';
import { LoginService } from '../shared/repositories/login.service'; 

@Component({
    selector: 'app-login',
    templateUrl: './login.component.html',
    styleUrls: ['./login.component.css']
})

export class LoginComponent implements OnInit {
    public username;
    public password;
    public loginString;
    @Output() loggedIn = new EventEmitter();
    private loggedInTemp;


    constructor(private ls: LoginService){

    }
    ngOnInit() {
	    this.username="";
	    this.password="";
      this.loggedInTemp = false;
    }

    onLogin(){
	    //this.ls.login(this.username,this.password);

      this.ls.login(this.username, this.password)
      .subscribe(resp => {
        this.loginString = resp.status;
        console.log(this.loginString);
        this.loggedInTemp = this.checkLogin(this.loginString);
        this.loggedIn.emit(this.loggedInTemp);
      });
    }

    checkLogin(status){
      if(status === "Successful login.")
      {
        return true;
      }
      return false;
    }
}
