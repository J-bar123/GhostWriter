
import { Injectable } from '@angular/core';

import {HttpClient} from '@angular/common/http';
import {User} from '../_models/user';
import {Observable} from "rxjs";

interface GoalSet{
  minutegoal: number;
  caloriegoal: number;
}



@Injectable({ providedIn: 'root' })
export class UserService {


  constructor(private http: HttpClient) { }

  getAll() {
     return this.http.get<User[]>(`http://localhost:3030/user/allusers`);
  }



  register(user: User) {
    return this.http.post(`http://localhost:3030/user/register`, user);
  }


  //TODOc: add a function that will allow users to set their calorie and minute goals.
  // The function will communicate with the back-end.
  setGoals(user: User){
    return this.http.post('http://localhost:3030/user/setgoals', user);
  }

  //TODOc: add a function that will allow users to get calorie and minute goals for a specific user
  // (this means, given a username, this function should fetch calories and minute goals for that user).
  // The function will communicate with the back-end.

  getGoals(name: User): Observable<User[]>{
    return this.http.get<User[]>('http://localhost:3030/user/getgoals/' + name.username);
  }


}

