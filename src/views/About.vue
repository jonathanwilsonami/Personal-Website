<template>
  <div class="about">
    <h1>About</h1>
    <div class="png-container">
      <img :src="aboutMe" alt="Me" class="resized-image" style="border-radius: 50%;">
    </div>
    <p>
    For most of my early life (from childhood through part of my undergrad) I worked in construction renovating 
    homes and eventually heavy civil. Then one day while installing moisture sensors for an irrigation system 
    I got a spark of inspiration to change my career trajectory to computers and data. I went on to study my 
    undergrad in Applied Statistics and Computer Science several years ago at BYU after which I jumped right 
    into working fulltime as a software engineer. I spent a few years working on a satellite software for space 
    situational awareness for the DoD focused mostly on image processing and optimization. I currently work in 
    cybersecurity using big data analytics and machine learning to track down bad guys.  
    </p>
    <p>
    I consider myself an engineer with expertise in software engineering and intelligent systems focused in the 
    area of cyber physical systems (IoT, software automation, AI/ML). I’m a Linux and Python native with almost 8 
    years of professional experience in both but I’m language and technology agnostic having learned many other 
    languages and technologies over the years. I’m mostly self-taught and hands-on projects based learner hence 
    why I love doing projects. If you would like to know more about my experience feel free to send a message, 
    look at my resume or browse my past projects.  
    </p>
    <div>
      <b-button href="https://drive.google.com/file/d/1v5sSKpOcu-SR-o12RCBp7coge8NKSBGV/view?usp=drive_link">Download Resume</b-button>
    </div>
    <h3>Interests</h3>
    <p>
      Reading, hiking in nature, tinkering, construction, traveling, olympic lifting and functional fitness.   
    </p>
    <h3>Lists</h3>
    <ul>
      <li><router-link to="/books">Good Books</router-link></li>
      <li><router-link to="/travel">Travel</router-link></li>
      <li><router-link to="/resources">Resources</router-link></li>
    </ul>
    <div class="contact-info">
      <h3>Contact Me</h3>
        <b-card title="Contact Info" >
          <b-card-text>
            <i class="material-icons orange600">location_on</i>
            Fairfax, Virginia 
          </b-card-text>
          <b-card-text>
            <i class="material-icons orange600">email</i>
            <a href="mailto:jonwilami@gmail.com">jonwilami@gmail.com</a> 
          </b-card-text>
          <b-card-text>
            <i class="material-icons">phone</i>
            540-335-6617 
          </b-card-text>
        </b-card>
    </div>
  </div>
</template>

<script>
import aboutMe from "../assets/img/meImg.png";
export default {
  name: "About",
  data() {
    return {
      aboutMe: aboutMe,
    };
  },
};
</script>

<style scoped>
.contact-info {
  margin-top: 2em;
  margin-bottom: 2em;
  text-decoration: none;

}
a.contact-info {
 text-decoration: none;
  
}
h3 {
  margin-top: 1em;
  margin-bottom: 1em;
}
.about {
  margin-right: 35em;
  margin-left: 35em;
} 
ol, ul {
    margin-left: 4em;
    padding: 0;
}
li {
  text-align: left;
}

.resized-image {
  width: 300px;
  height: 430px;
  object-fit: cover; 
}

/* @Media Queries */

/* Margin spacing */
@media only screen and (max-width: 1700px) {
  .about {
    margin-right: 0;
    margin-left: 0;
  }
  ol, ul {
    margin-left: 1em;
    padding: 0;
  }
}


</style>
