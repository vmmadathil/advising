import { Component, OnInit, Input } from '@angular/core';

@Component({
  selector: 'app-name-button',
  templateUrl: './name-button.component.html',
  styleUrls: ['./name-button.component.css']
})
export class NameButtonComponent implements OnInit {
  @Input() name;
  constructor() { }

  ngOnInit() {
  }

}