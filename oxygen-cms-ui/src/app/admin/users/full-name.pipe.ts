import {Pipe, PipeTransform} from '@angular/core';

@Pipe({ name: 'fullName' })

export class FullNamePipe implements PipeTransform {
  transform(users: any[]) {
    return users.map(user => {
      user.fullName = `${user.name.first} ${user.name.last}`;
      return user;
    });
  }
}
