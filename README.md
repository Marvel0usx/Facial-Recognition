# Facial Recognition - An experiment with Logistic Regression
Using logistic regression model to solve some real-world problems, we can explorer different possibilities and outcomes.

### Question Answered by Logistic Regression

Similar to linear regression, logistic regression maps elements in the input space the to discrete outputs. It answers what the (log odds of) probability that an array of grayscale pixels from human face represents a certain gender, age, and ethnicity.

### Alternative

Decision tree/random forest can also be used to solve this problem since these models work well with the dataset used here.

### Data Scraping - *Scrapy*

Initialize project: `scrapy startproject mySpider`

Start scraping: `scrapy runspider mySpider.py`

<img src="demo\scrapy_architecture.png" alt="scrapy_arch" style="zoom:50%;float:left" />

### Dataset

The dataset is obtained from scraping the page https://generated.photos/faces/. The images are downloaded, stored in *MongoDB* and to reduce the pressure to my laptop, they are resized to 64x64 and made into grayscale. Labels are extracted from the link to image, and they're stored along with the link to image. The outline of the database is shown below. (key resembles what is in the dataset)

| key         | type      | note                                                         |
| ----------- | --------- | ------------------------------------------------------------ |
| pixels      | List[$x$] | $x \in [0, 255]$                                             |
| gender      | str       | gender $\in \{\text{male}, \text{female}\}$                  |
| age         | str       | age $\in \{\text{infant}, \text{young-adult}, \text{adult}, \text{middle-aged}\}$ |
| ethnicity   | str       | ethnicity $\in \{\text{asian}, \text{black}, \text{latino}, \text{white}\}$ |
| emotion     | str       | emotion $\in \{\text{joy}, \text{neutral}\}$                 |
| hair_color  | str       | hair_color $\in \{ \text{brown}, \text{black}, \text{gray}, \text{blond}\}$ |
| eye_color   | str       | eye_color $\in \{ \text{brown}, \text{blue}, \text{gray}, \text{green}\}$ |
| hair_length | str       | hair_length $\in \{ \text{short}, \text{medium}, \text{long}\}$ |

Please contact me to acquire the dataset :)

## Training Outputs

- Identify gender

  <img src="demo\gender.jpg" alt="gender" style="zoom:50%;float:left" />

- Identify age

  <img src="demo\age.jpg" alt="age" style="zoom:50%;float:left" />

- Identify ethnicity

  <img src="demo\ethnicity.jpg" alt="ethnicity" style="zoom:50%;float:left" />

## Demo

Run `python visualizer.py` to discover!

### Further Improvement

- Train with RGB data since it has better result in predicting *eye_color*, *hair_color*, and *ethnicity*.
- Try using `scrapy_splash` to render JS.
- Implement a decision tree for the same sake.

