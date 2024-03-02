<template>
  <div class="books">
    <h1>Favorite books</h1>
    <div v-for="(books, genre) in booksByGenre" :key="genre" class="genre">
      <h2>{{ genre }}</h2>
      <ol class="book-list">
        <li v-for="book in books" :key="book.id" class="book">
          {{ book.title }}: <a :href="book.amazonLink" target="_blank">Amazon</a>
        </li>
      </ol>
    </div>
    <h3>More to come...</h3>
  </div>
</template>

<script>
export default {
  name: "Books",
  data() {
    return {
      booksByGenre: {
        "Technology": [
          { id: 1, title: "Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow: Concepts, Tools, and Techniques to Build Intelligent Systems", author: "Author 1", amazonLink: "https://www.amazon.com/Hands-Machine-Learning-Scikit-Learn-TensorFlow/dp/1098125975/ref=sr_1_1?crid=1VICJVE4N8F2E&dib=eyJ2IjoiMSJ9.0Jm1bLoXUBA_cK-tar7HW8sLaoBiOLb0vLV9cGgPunrGjHj071QN20LucGBJIEps.M88JwFgBk9tCmIy6YBpL2x283StVoRMKF9j7Dg70PUo&dib_tag=se&keywords=Hands-On+Machine+Learning+with+Scikit-Learn+and+TensorFlow%3A+Concepts%2C+Tools%2C+and+Techniques+to+Build+Intelligent+Systems+2nd&qid=1707951570&s=books&sprefix=hands-on+machine+learning+with+scikit-learn+and+tensorflow+concepts%2C+tools%2C+and+techniques+to+build+intelligent+systems+2nd+%2Cstripbooks%2C54&sr=1-1" },
          { id: 2, title: "Superintelligence: Paths, Dangers, Strategies", author: "Author 2", amazonLink: "https://www.amazon.com/Superintelligence-Dangers-Strategies-Nick-Bostrom/dp/0199678111/ref=asc_df_0199678111/?tag=hyprod-20&linkCode=df0&hvadid=312060980065&hvpos=&hvnetw=g&hvrand=5897199288616909501&hvpone=&hvptwo=&hvqmt=&hvdev=c&hvdvcmdl=&hvlocint=&hvlocphy=1027243&hvtargid=pla-435516797885&psc=1&mcid=bdc9465a99db380a886a0ad4bc96ce67&gclid=Cj0KCQiA5rGuBhCnARIsAN11vgQA25g_rr3JrsDoawsmHUNkItdXyRsA7mA04Y1h_9S_eMOg58pnye4aAluBEALw_wcB" }
        ],
        "Building Architecture": [
          { id: 3, title: "The Architecture Reference & Specification Book updated & revised: Everything Architects Need to Know Every Day", author: "Author 3", amazonLink: "https://www.amazon.com/Architecture-Reference-Specification-updated-revised/dp/163159379X/ref=sr_1_4?crid=2GLUL4ANJM06W&dib=eyJ2IjoiMSJ9.gbnGvKqYjTfHVJ2I2TD2cW5iSxLpzYaqoQrobNhAOnz4AGmt6h3rkSy04fY2WFjm45VffP0bx1kuh-zgZ1pAyrQUZfVeCRqSl_L4JacXfou_JYWJEg3LaIE4rddtvdoK5UrObCTr3brj0veD8Z6bq2-Ox-4v3mooBQwO1yAxaaNil135NSL4JP_LuJo498lTIS-TUNN3YzqPXB6M74yBGxAbFPHxkev222BH6cLx7q_nSD8tt4vw05YT1CO4IJscF2x7XlbFFIhQ33J-GWZ3DX1hWUd1ZSg4TX585lq-FeY.0OudIGKuOCxZxktu_b8Wrvf2akICje7krV3IWbmmgsM&dib_tag=se&keywords=architecture+books&qid=1707951788&s=books&sprefix=Architec%2Cstripbooks%2C58&sr=1-4" },
          { id: 4, title: "Architecture: Form, Space, and Order", author: "Author 4", amazonLink: "https://www.amazon.com/dp/0471752169?psc=1&ref=ppx_yo2ov_dt_b_product_details" }
        ]
        // Add more genres and books here
      }
    };
  }
};
</script>

<style scoped>
.books {
  display: block; /* Ensure this is block to avoid flex issues */
  padding: 0;
  margin: 0;
}

.genre {
  display: block; /* Confirm this is block for proper flow */
  padding: 0;
  margin: 0 0 20px; /* Add bottom margin for spacing between genres */
}

.book-list {
  list-style-type: decimal; /* Explicitly set list style */
  list-style-position: outside; /* Ensure numbers are outside items */
  padding-left: 40px; /* Adjust as needed to align numbers */
  margin: 0;
}

.book {
  margin: 0; /* Reset to ensure clean alignment */
}
</style>