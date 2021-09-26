import { Component, OnDestroy, OnInit } from "@angular/core";
import { first, mergeMap } from "rxjs/operators";

import { NotificationService } from "../_services/notification.service";
import { UserService } from "../_services/user.service";
import { User } from "../_models/user";
import { FormControl } from '@angular/forms';
import { Observable } from 'rxjs';
import { ReviewService } from "../_services/review.service";
import { ActivatedRoute, Router } from "@angular/router";



import {from} from "rxjs";
import {Review} from "../_models/Review";


@Component({
  templateUrl: "home.component.html",

  styleUrls: ["home.component.css"],
})


export class HomeComponent implements OnInit {
  homeUser: User;

  query: string;
  SearchControl = new FormControl({value: "", disabled: false});

  filteredOptions: Observable<string[]>;
  allPlaces: Review[];
  autoCompleteList: any[];

  constructor(
    private router: Router,
    private notifService: NotificationService,
    private userService: UserService,
    private reviewService: ReviewService
  ) {}
 

  ngOnInit() {
    this.reviewService.getAll().subscribe(places => {
      this.allPlaces = places;
    });
  }

  goToForm(event: Event) {
    let elementId: string = (event.target as Element).id;

    console.log(elementId)

    // let route = this.router.config.find((r) => r.path === 'new');
    // route.data = { rapper: elementId };
    this.router.navigate(['/new', elementId]);
  }
}
