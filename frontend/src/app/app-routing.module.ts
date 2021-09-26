import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import {HomeComponent} from './home/home.component';

import {Role} from './_models/role';
import {CreateComponent} from './create/create.component';


// TODOc: add the route to the 'settings' component.

const routes: Routes = [{path: '', component: HomeComponent},
  {path: 'new/:rapper', component: CreateComponent}];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
