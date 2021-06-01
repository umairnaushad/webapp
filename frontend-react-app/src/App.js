import React from 'react';

class UserProfiles extends React.Component {
  constructor(){
    super();
    this.state = {
      //name: {title: '', first: '', last: ''},
      user: {id: '', username: '', email: ''}
      //image: ''
    };
    // fix the this value
    this.getUser = this.getUser.bind(this);
  }

  componentWillMount() {
    this.getUser();
  }

  getUser() {
    //fetch('https://randomuser.me/api/')
    fetch('http://127.0.0.1:5000/api/v1/resources/users/ById/11')
    
    //fetch('http://localhost:5000/query-example?id=20')
    .then(response => {
      if(response.ok) return response.json();
      throw new Error('Request failed.');
    })
    .then(data => {
      this.setState({user: data.user});
    })
    .catch(error => {
      console.log(error);
    });
  }

  render() {
    return (
	<div>
          <h1>{`${this.state.user.id} ${this.state.user.username} ${this.state.user.email}`}</h1>
          <button onClick={this.getUser}>Get new user.</button>
	</div>
    );
  }
}

export default UserProfiles;