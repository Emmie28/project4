
document.addEventListener('DOMContentLoaded', function(){
  
  document.querySelector('#all-posts').style.display = 'block';
  document.querySelector('#new-post').style.display = 'none';
  document.querySelector("#user-posts").style.display = 'none';
  
  document.querySelector('#new_post').addEventListener('click', () => {
    new_post();
  }); 
  
  document.querySelector('#post_form').onsubmit = post;
  
});

// Function to render new post form.
function new_post(){
  document.querySelector('#all-posts').style.display = 'none';
  document.querySelector('#u_details').style.display = 'none';
  document.querySelector('#new-post').style.display = 'block';
  document.querySelector("#user-posts").style.display = 'none';
  return false;
}

// Function to handle follow and unfollow.
function follow(name){
  let x = document.getElementById('user').textContent;
  let y = document.getElementById('ff_btn').textContent;
  

  fetch(`/details/${name}`, {
      method: 'PUT',
      body: JSON.stringify({
      followers : x,
      btn : y
      })

  });
  
  // Wait for fetch to return before calling user_details function.
  setTimeout(() => {user_details(name);}, 100);
  localStorage.clear();
  return false;
} 


//Function to post a message
function post(){
  
  // Get the values of post and name respectively.
  const post = document.querySelector('#text').value;
  const name = document.querySelector('#user').value;

  // Post the new message to the server.
  fetch('/post', {
      method: 'POST',
      body: JSON.stringify({
        name: name,
        post: post, 
      })
    })
    .then(response => response.json())
    .then(result => {
      // Print result
      console.log(result);
  });
  
}



// Function to handle the details of each user.
 function user_details(name){
  // Get the name of the logged in user.
  let x = document.getElementById('user').textContent;
  let a = document.querySelector('#ff_btn');
  let b = document.getElementById('ff_btn').textContent;
  
  if (b.trimLeft() === 'follow'){
    a.innerHTML = 'unfollow';
    }
  else{
      a.innerHTML = 'follow';
    }

  fetch(`/details/${name}`)
  .then(response => response.json())
  .then(details => {
    console.log(details);
  
    // Handle details
    let ct = 0;
    let cp = 0;
    
  for (let i = 0; i < details.length; i++){
      var followers = details[i].followers;
      var following = details[i].following;
     
      if (followers === x ){
        check = true;
      }
      if (following != 'names'){
        cp++;
      }
      if (followers != 'names'){
        ct++;
      }
  }

    let doc = document.querySelector("#user_following");
    setTimeout(() => {doc.innerHTML=`${ct} followers  ${cp} following`;}, 100);
    
    
});
localStorage.clear();
return false;
}

// Function to edit a post.
function edit(){
  // Get the content of the message you want to edit.
  new_content = document.querySelector("#text").value;
  fetch(`/edit_post1`, {
    method: 'PUT',
    body: JSON.stringify({
       posts : new_content
    })
    
  });
  localStorage.clear();
  return false;
}

// Function to handle likes and unlikes of a post.
function like_unlike(x,id) {
  // Get the state of the like_unlike icon.
  let y = x.classList.contains('fa-thumbs-down');
  x.classList.toggle("fa-thumbs-down");
  var state;
  if (y === true){
    state = 'up';
  }
  else{
    state = 'down';
  }
  
  fetch(`/like_unlike/${id}`,{
    method: 'PUT',
      body: JSON.stringify({
        id : id,
        state : state
    })
  
  });
  
  setTimeout(() => {update_like_unlike(id);}, 100);
}


function update_like_unlike(id) {
  document.getElementById(`${id}`).innerHTML ='';

  fetch(`/like_unlike/${id}`,)
  .then(response => response.json())
  .then(l => {
    console.log(l);
    
    var ct = l.likes;
  
    setTimeout(() => {document.getElementById(`${id}`).innerHTML=`${ct}`;}, 100);
  
  });
  localStorage.clear();
}



