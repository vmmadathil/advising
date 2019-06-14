import { Injectable } from "@angular/core";
import { Observable } from "rxjs";
import { HttpClient, HttpHeaders } from "@angular/common/http";
import { catchError } from 'rxjs/operators';


@Injectable()
export class LoginService {
  protected endpoint = "https://DetailedLinenFact--vmadathil.repl.co/"

  protected httpOptions = {
    headers: new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': 'mominirfan'
    })
  };

  constructor(
    protected httpClient: HttpClient
  ) {}

  login(user,pass): Observable<any> {
    return this.httpClient.get<any>(`${this.endpoint}login?username=${user}&password=${pass}`, this.httpOptions);
  }

  getUsers(): Observable<any> {
    let request = `${this.endpoint}users`;
    return this.httpClient.get<any>(request, this.httpOptions);
  }

  protected handleException(exception: any) {
    var message = `${exception.status} : ${exception.statusText}\r\n${exception.message}`;
    alert(message);
    return Observable.throw(exception);
  }


}
