// TODO
import { Component, OnInit } from "@angular/core";
import { FormControl, Validators, FormGroup } from "@angular/forms";

import { NotificationService } from "../_services/notification.service";
import { first } from "rxjs/operators";
import { User } from "../_models/user";
import { mergeMap } from 'rxjs/operators';

import { AuthService } from "../_services/auth.service";
import { ReviewService } from "../_services/review.service";
import { ActivatedRoute, Router } from "@angular/router";
import { SongService } from "../_services/song.service";
import { Track } from 'ngx-audio-player';   

@Component({
  selector: "app-create",
  templateUrl: "./create.component.html",
  styleUrls: ["./create.component.css"],
})
export class CreateComponent implements OnInit {
  date: Date;
  rapper: string;

  minutes: number;
  calories: number;

  description: string;
  location: string;
  loading: boolean;
  tempAr: string;

  msaapDisplayTitle = true;
msaapDisplayPlayList = false;
msaapPageSizeOptions = [2,4,6];
msaapDisplayVolumeControls = true;
msaapDisplayRepeatControls = true;
msaapDisplayArtist = false;
msaapDisplayDuration = false;
msaapDisablePositionSlider = true;
   
// Material Style Advance Audio Player Playlist
msaapPlaylist: Track[] = [
];


  locationCntrl = new FormControl({ value: "", disabled: false });

  edit: boolean;
  sub: any;

  public remainingWords = 100;

  public textareaForm = new FormGroup({
    textinput: new FormControl(),
  });

  wordCounter() {
    this.remainingWords = this.textareaForm.value
      ? 150 - this.textareaForm.value.textinput.split(/\s+/).length
      : 100;
    if (this.remainingWords <= 0) {
      this.textareaForm.controls["textinput"].disable();
    }
  }

  constructor(
    private songService: SongService,
    private route: ActivatedRoute,
    private router: Router,
    private notifService: NotificationService
  ) {}

  ngOnInit() {
    this.hideloader();
    document.getElementById("audioph").style.display = "none";
    this.sub = this.route.params.subscribe((params) => {
      this.rapper = params["rapper"];
      this.loading = false;
      // this.textareaForm.patchValue({textinput: "yo yo yo yo"})

      this.tempAr = params["rapper"];

      if (this.rapper === "kanye") {
        this.rapper = "Kanye West";
      } else if (this.rapper === "nas") {
        this.rapper = "Nas";
      } else if (this.rapper === "biggie") {
        this.rapper = "The Notorious B.I.G";
      } else if (this.rapper === "jayz") {
        this.rapper = "Jay-Z";
      } else if (this.rapper === "rickRoss") {
        this.rapper = "Rick Ross";
      } else if (this.rapper === "kendrick") {
        this.rapper = "Kendrick Lamar";
      } else if (this.rapper === "50cent") {
        this.rapper = "50 Cent";
      }

      this.locationCntrl = new FormControl({
        value: this.rapper,
        disabled: true,
      });
    });
  }

  generateLyrics() {
    // this.textareaForm.patchValue({textinput: "yo yo yo yo"})
  }

  // Function is defined
  hideloader() {
    // Setting display of spinner
    // element to none
    document.getElementById("loading").style.display = "none";
  }

  setupPlay(url) { 
    document.getElementById("audioph").style.display = "initial";
    this.msaapPlaylist.push({
      title: '',
      link: url,
      artist: this.rapper,
      duration: 30
    })
  }

  save() {

    if (this.textareaForm.value.textinput === null) {
      this.notifService.showNotif("Please fill out the form", "OK");
      return;
    } 

    document.getElementById("loading").style.display = "initial";
    
    var pace = 1.0;

    if (this.rapper === "kanye") {
      pace = 0.85;
    } else if (this.rapper === "nas") {
      pace = 0.85;
    } else if (this.rapper === "biggie") {
      pace = 0.9;
    } else if (this.rapper === "jayz") {
      pace = 0.8;
    } else if (this.rapper === "rickRoss") {
      this.tempAr = "ross";
    } else if (this.rapper === "kendrick") {
      this.tempAr = "kendrick";
    }

    var data = {
      "artist": this.tempAr,
      "lyrics": this.textareaForm.value.textinput,
      "pace": pace,
    };

    this.songService.getVocals(data).pipe(
      mergeMap(response => this.songService.mergeVocals({"artist": this.tempAr, "url":response.Url}))
    ).subscribe(res => {
      this.hideloader();
      if (res.Success != null) {
        this.notifService.showNotif(res.Url, "OK");
        this.setupPlay(res.Url)
      } else { 
        this.notifService.showNotif("Error", "OK");
        console.log(res);
      }
    });



    

    //TODO:
    // this.router.navigate(["/"]);
  }


  updateCals(e) {
    this.calories = e.target.value;
  }

  generate() {
    this.songService.generateLyrics({"artist": this.tempAr}).subscribe(res => {
      if (res.Success != null) {
        this.textareaForm.patchValue({textinput: res.Url})
      } else { 
        this.notifService.showNotif("Error", "OK");
      }
    });

  }

  updateLocation(e) {}

  updateDesription(e) {
    this.description = e.target.value;
  }
}
