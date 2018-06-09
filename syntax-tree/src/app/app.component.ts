import {Component, OnInit} from '@angular/core';
import {HttpClient} from "@angular/common/http";

@Component({
  selector: 'app-root',
  template: `
      <tree-root [nodes]="nodes" [options]="options">
          <ng-template #treeNodeTemplate let-node let-index="index">
              <span>{{ node.data.name }}</span>
              <span *ngIf="node.data.content" style="background: rgba(225,225,225,0.99)">
                  &nbsp;{{node.data.content}}&nbsp;
              </span>
          </ng-template>
      </tree-root>
  `,
  styles: []
})
export class AppComponent implements OnInit{
  constructor(
    private http: HttpClient
  ){}

  nodes = [];

  ngOnInit(){
    this.http.get('/assets/syntax-tree.json').toPromise().then((data) => {
      this.nodes = [data];
    });
  }

  // nodes = [
  //   {
  //     id: 1,
  //     name: 'root1',
  //     children: [
  //       { id: 2, name: 'child1' },
  //       { id: 3, name: 'child2' }
  //     ]
  //   },
  //   {
  //     id: 4,
  //     name: 'root2',
  //     children: [
  //       { id: 5, name: 'child2.1' },
  //       {
  //         id: 6,
  //         name: 'child2.2',
  //         children: [
  //           { id: 7, name: 'subsub' }
  //         ]
  //       }
  //     ]
  //   }
  // ];
  options = {};
}
