import { Injectable } from "@angular/core";

import { HttpClient } from "@angular/common/http";
import { Observable } from "rxjs";
import { SongType } from "../_models/SongType";

@Injectable({ providedIn: "root" })
export class SongService {
  constructor(private http: HttpClient) {}

  getVocals(data) {
    return this.http.post<SongType>(
      "https://shellhacks-327117.ue.r.appspot.com/songs/getVocals/",
      JSON.stringify(data)
    );
  }

  mergeVocals(data) {
    return this.http.post<SongType>(
      "https://shellhacks-327117.ue.r.appspot.com/songs/combineSong/",
      JSON.stringify(data)
    );
  }

  generateLyrics(data) {
    return this.http.post<SongType>(
      "https://shellhacks-327117.ue.r.appspot.com/lyrics/generate/",
      JSON.stringify(data)
    );
  }
}
