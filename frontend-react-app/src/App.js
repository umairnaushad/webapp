import React from 'react';

class UserProfiles extends React.Component {
  constructor(){
    super();
    this.state = {
      users: [{id: '', username: '', email: ''}]
    };
    // fix the this value
    this.getUser = this.getUser.bind(this);
  }

  componentWillMount() {
    //this.getUser(12);
    this.getAllUsers();
  }

  getUser(userId) {
    fetch('http://127.0.0.1:5000/api/v1/resources/users/ById/' + userId)
    .then(response => {
      if(response.ok) return response.json();
      throw new Error('Request failed.');
    })
    .then(data => {
      this.setState({users: data.users[0]});
    })
    .catch(error => {
      console.log(error);
    });
  }

  getAllUsers() {
    fetch('http://127.0.0.1:5000/api/v1/resources/users')
    .then(response => {
      if(response.ok) return response.json();
      throw new Error('Request failed.');
    })
    .then(data => {
      this.setState({users: data.users});
    })
    .catch(error => {
      console.log(error);
    });
  }

  render() {
    return (
  <div>
    <h1>Get All Users </h1>
    <ul>
    <li>Id  User Name   Email</li>
      {this.state.users.map((user, index) => (
        <li key={index}>{user.id}   {user.username}   {user.email}</li>
      ))}
    </ul>
    <button onClick={this.getUser}>Get new user.</button>
  </div>
    );
  }
}

export default UserProfiles;