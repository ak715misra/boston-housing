
# coding: utf-8

# # Machine Learning Engineer Nanodegree
# ## Model Evaluation & Validation
# ## Project: Predicting Boston Housing Prices
# 
# Welcome to the first project of the Machine Learning Engineer Nanodegree! In this notebook, some template code has already been provided for you, and you will need to implement additional functionality to successfully complete this project. You will not need to modify the included code beyond what is requested. Sections that begin with **'Implementation'** in the header indicate that the following block of code will require additional functionality which you must provide. Instructions will be provided for each section and the specifics of the implementation are marked in the code block with a 'TODO' statement. Please be sure to read the instructions carefully!
# 
# In addition to implementing code, there will be questions that you must answer which relate to the project and your implementation. Each section where you will answer a question is preceded by a **'Question X'** header. Carefully read each question and provide thorough answers in the following text boxes that begin with **'Answer:'**. Your project submission will be evaluated based on your answers to each of the questions and the implementation you provide.  
# 
# >**Note:** Code and Markdown cells can be executed using the **Shift + Enter** keyboard shortcut. In addition, Markdown cells can be edited by typically double-clicking the cell to enter edit mode.

# ## Getting Started
# In this project, you will evaluate the performance and predictive power of a model that has been trained and tested on data collected from homes in suburbs of Boston, Massachusetts. A model trained on this data that is seen as a *good fit* could then be used to make certain predictions about a home — in particular, its monetary value. This model would prove to be invaluable for someone like a real estate agent who could make use of such information on a daily basis.
# 
# The dataset for this project originates from the [UCI Machine Learning Repository](https://archive.ics.uci.edu/ml/datasets/Housing). The Boston housing data was collected in 1978 and each of the 506 entries represent aggregated data about 14 features for homes from various suburbs in Boston, Massachusetts. For the purposes of this project, the following preprocessing steps have been made to the dataset:
# - 16 data points have an `'MEDV'` value of 50.0. These data points likely contain **missing or censored values** and have been removed.
# - 1 data point has an `'RM'` value of 8.78. This data point can be considered an **outlier** and has been removed.
# - The features `'RM'`, `'LSTAT'`, `'PTRATIO'`, and `'MEDV'` are essential. The remaining **non-relevant features** have been excluded.
# - The feature `'MEDV'` has been **multiplicatively scaled** to account for 35 years of market inflation.
# 
# Run the code cell below to load the Boston housing dataset, along with a few of the necessary Python libraries required for this project. You will know the dataset loaded successfully if the size of the dataset is reported.

# In[1]:


# Import libraries necessary for this project
import numpy as np
import pandas as pd

# Import supplementary visualizations code visuals.py
import visuals as vs

# Pretty display for notebooks
get_ipython().run_line_magic('matplotlib', 'inline')

# Load the Boston housing dataset
data = pd.read_csv('housing.csv')
prices = data['MEDV']
features = data.drop('MEDV', axis = 1)
    
# Success
print("Boston housing dataset has {} data points with {} variables each.".format(*data.shape))
print(data.describe())


# ## Data Exploration
# In this first section of this project, you will make a cursory investigation about the Boston housing data and provide your observations. Familiarizing yourself with the data through an explorative process is a fundamental practice to help you better understand and justify your results.
# 
# Since the main goal of this project is to construct a working model which has the capability of predicting the value of houses, we will need to separate the dataset into **features** and the **target variable**. The **features**, `'RM'`, `'LSTAT'`, and `'PTRATIO'`, give us quantitative information about each data point. The **target variable**, `'MEDV'`, will be the variable we seek to predict. These are stored in `features` and `prices`, respectively.

# ### Implementation: Calculate Statistics
# For your very first coding implementation, you will calculate descriptive statistics about the Boston housing prices. Since `numpy` has already been imported for you, use this library to perform the necessary calculations. These statistics will be extremely important later on to analyze various prediction results from the constructed model.
# 
# In the code cell below, you will need to implement the following:
# - Calculate the minimum, maximum, mean, median, and standard deviation of `'MEDV'`, which is stored in `prices`.
#   - Store each calculation in their respective variable.

# In[2]:


# Minimum price of the data
minimum_price = np.min(prices)

# Maximum price of the data
maximum_price = np.max(prices)

# Mean price of the data
mean_price = np.mean(prices)

# Median price of the data
median_price = np.median(prices)

# Standard deviation of prices of the data
std_price = np.std(prices)

# Average number of rooms in the house
mean_rooms = np.mean(features['RM'])

# Show the calculated statistics
print("Statistics for Boston housing dataset:\n")
print("Minimum price: ${}".format(minimum_price)) 
print("Maximum price: ${}".format(maximum_price))
print("Mean price: ${}".format(mean_price))
print("Median price ${}".format(median_price))
print("Standard deviation of prices: ${}".format(std_price))
print("Mean rooms: {}".format(mean_rooms))


# ### Question 1 - Feature Observation
# As a reminder, we are using three features from the Boston housing dataset: `'RM'`, `'LSTAT'`, and `'PTRATIO'`. For each data point (neighborhood):
# - `'RM'` is the average number of rooms among homes in the neighborhood.
# - `'LSTAT'` is the percentage of homeowners in the neighborhood considered "lower class" (working poor).
# - `'PTRATIO'` is the ratio of students to teachers in primary and secondary schools in the neighborhood.
# 
# 
# ** Using your intuition, for each of the three features above, do you think that an increase in the value of that feature would lead to an **increase** in the value of `'MEDV'` or a **decrease** in the value of `'MEDV'`? Justify your answer for each.**
# 
# **Hint:** This problem can phrased using examples like below.  
# * Would you expect a home that has an `'RM'` value(number of rooms) of 6 be worth more or less than a home that has an `'RM'` value of 7?
# * Would you expect a neighborhood that has an `'LSTAT'` value(percent of lower class workers) of 15 have home prices be worth more or less than a neighborhood that has an `'LSTAT'` value of 20?
# * Would you expect a neighborhood that has an `'PTRATIO'` value(ratio of students to teachers) of 10 have home prices be worth more or less than a neighborhood that has an `'PTRATIO'` value of 15?

# **Answer: ** Increase in the value of RM should lead to increase in MEDV. Increase in the value of LSTAT should lower MEDV. Increase in the value of PTRATIO should also lower MEDV.

# ----
# 
# ## Developing a Model
# In this second section of the project, you will develop the tools and techniques necessary for a model to make a prediction. Being able to make accurate evaluations of each model's performance through the use of these tools and techniques helps to greatly reinforce the confidence in your predictions.

# ### Implementation: Define a Performance Metric
# It is difficult to measure the quality of a given model without quantifying its performance over training and testing. This is typically done using some type of performance metric, whether it is through calculating some type of error, the goodness of fit, or some other useful measurement. For this project, you will be calculating the [*coefficient of determination*](http://stattrek.com/statistics/dictionary.aspx?definition=coefficient_of_determination), R<sup>2</sup>, to quantify your model's performance. The coefficient of determination for a model is a useful statistic in regression analysis, as it often describes how "good" that model is at making predictions. 
# 
# The values for R<sup>2</sup> range from 0 to 1, which captures the percentage of squared correlation between the predicted and actual values of the **target variable**. A model with an R<sup>2</sup> of 0 is no better than a model that always predicts the *mean* of the target variable, whereas a model with an R<sup>2</sup> of 1 perfectly predicts the target variable. Any value between 0 and 1 indicates what percentage of the target variable, using this model, can be explained by the **features**. _A model can be given a negative R<sup>2</sup> as well, which indicates that the model is **arbitrarily worse** than one that always predicts the mean of the target variable._
# 
# For the `performance_metric` function in the code cell below, you will need to implement the following:
# - Use `r2_score` from `sklearn.metrics` to perform a performance calculation between `y_true` and `y_predict`.
# - Assign the performance score to the `score` variable.

# In[3]:


# Import 'r2_score'
from sklearn.metrics import r2_score
def performance_metric(y_true, y_predict):
    """ Calculates and returns the performance score between 
        true and predicted values based on the metric chosen. """
    
    # Calculate the performance score between 'y_true' and 'y_predict'
    score = r2_score(y_true, y_predict)
    
    # Return the score
    return score


# ### Question 2 - Goodness of Fit
# Assume that a dataset contains five data points and a model made the following predictions for the target variable:
# 
# | True Value | Prediction |
# | :-------------: | :--------: |
# | 3.0 | 2.5 |
# | -0.5 | 0.0 |
# | 2.0 | 2.1 |
# | 7.0 | 7.8 |
# | 4.2 | 5.3 |
# 
# Run the code cell below to use the `performance_metric` function and calculate this model's coefficient of determination.

# In[4]:


# Calculate the performance of this model
score = performance_metric([3, -0.5, 2, 7, 4.2], [2.5, 0.0, 2.1, 7.8, 5.3])
print("Model has a coefficient of determination, R^2, of {:.3f}.".format(score))


# * Would you consider this model to have successfully captured the variation of the target variable? 
# * Why or why not?
# 
# ** Hint: **  The R2 score is the proportion of the variance in the dependent variable that is predictable from the independent variable. In other words:
# * R2 score of 0 means that the dependent variable cannot be predicted from the independent variable.
# * R2 score of 1 means the dependent variable can be predicted from the independent variable.
# * R2 score between 0 and 1 indicates the extent to which the dependent variable is predictable. An 
# * R2 score of 0.40 means that 40 percent of the variance in Y is predictable from X.

# **Answer:** R2 Score of 0.923 simply means 90% of the variance in the prices are predictable from the 3 features RM, PTRATIO and LSTAT.

# ### Implementation: Shuffle and Split Data
# Your next implementation requires that you take the Boston housing dataset and split the data into training and testing subsets. Typically, the data is also shuffled into a random order when creating the training and testing subsets to remove any bias in the ordering of the dataset.
# 
# For the code cell below, you will need to implement the following:
# - Use `train_test_split` from `sklearn.cross_validation` to shuffle and split the `features` and `prices` data into training and testing sets.
#   - Split the data into 80% training and 20% testing.
#   - Set the `random_state` for `train_test_split` to a value of your choice. This ensures results are consistent.
# - Assign the train and testing splits to `X_train`, `X_test`, `y_train`, and `y_test`.

# In[5]:


# Import 'train_test_split'
from sklearn.model_selection import train_test_split
import random
random.seed(8)
# TODO: Shuffle and split the data into training and testing subsets
X_train, X_test, y_train, y_test = train_test_split(features, prices, test_size=0.20, random_state=8)

# Success
print("Training and testing split was successful.")


# ### Question 3 - Training and Testing
# 
# * What is the benefit to splitting a dataset into some ratio of training and testing subsets for a learning algorithm?
# 
# **Hint:** Think about how overfitting or underfitting is contingent upon how splits on data is done.

# **Answer: ** Dataset is split into training and testing subsets because learning algorithm needs some check whether it's too simplistic (underfitting) or too complicated (overfitting). So it's first run on a part of dataset called training set, where it learns the patterns from the data. Then it applies this learning to the remaining part of the dataset called testing set to see how well it did.

# ----
# 
# ## Analyzing Model Performance
# In this third section of the project, you'll take a look at several models' learning and testing performances on various subsets of training data. Additionally, you'll investigate one particular algorithm with an increasing `'max_depth'` parameter on the full training set to observe how model complexity affects performance. Graphing your model's performance based on varying criteria can be beneficial in the analysis process, such as visualizing behavior that may not have been apparent from the results alone.

# ### Learning Curves
# The following code cell produces four graphs for a decision tree model with different maximum depths. Each graph visualizes the learning curves of the model for both training and testing as the size of the training set is increased. Note that the shaded region of a learning curve denotes the uncertainty of that curve (measured as the standard deviation). The model is scored on both the training and testing sets using R<sup>2</sup>, the coefficient of determination.  
# 
# Run the code cell below and use these graphs to answer the following question.

# In[6]:


# Produce learning curves for varying training set sizes and maximum depths
vs.ModelLearning(features, prices)


# ### Question 4 - Learning the Data
# * Choose one of the graphs above and state the maximum depth for the model. 
# * What happens to the score of the training curve as more training points are added? What about the testing curve? 
# * Would having more training points benefit the model? 
# 
# **Hint:** Are the learning curves converging to particular scores? Generally speaking, the more data you have, the better. But if your training and testing curves are converging with a score above your benchmark threshold, would this be necessary?
# Think about the pros and cons of adding more training points based on if the training and testing curves are converging.

# **Answer: ** I would like to pick one with max_depth=10.
# With the addition of more training points, score of training curve will not change since there is already no uncertainty about the curve and it's doing pretty good, but it would continue to perform badly on testing curve since uncertainty remains there and no improvements in the score. So it's a case of overfitting and adding more training points would not help.

# ### Complexity Curves
# The following code cell produces a graph for a decision tree model that has been trained and validated on the training data using different maximum depths. The graph produces two complexity curves — one for training and one for validation. Similar to the **learning curves**, the shaded regions of both the complexity curves denote the uncertainty in those curves, and the model is scored on both the training and validation sets using the `performance_metric` function.  
# 
# ** Run the code cell below and use this graph to answer the following two questions Q5 and Q6. **

# In[7]:


vs.ModelComplexity(X_train, y_train)


# ### Question 5 - Bias-Variance Tradeoff
# * When the model is trained with a maximum depth of 1, does the model suffer from high bias or from high variance? 
# * How about when the model is trained with a maximum depth of 10? What visual cues in the graph justify your conclusions?
# 
# **Hint:** High bias is a sign of underfitting(model is not complex enough to pick up the nuances in the data) and high variance is a sign of overfitting(model is by-hearting the data and cannot generalize well). Think about which model(depth 1 or 10) aligns with which part of the tradeoff.

# **Answer: **Model suffers from high bias when trained with a max depth of 1.
# Model suffers from high variance when trained with a max depth of 10. High Training score and Low Validation score point to this conclusion.

# ### Question 6 - Best-Guess Optimal Model
# * Which maximum depth do you think results in a model that best generalizes to unseen data? 
# * What intuition lead you to this answer?
# 
# ** Hint: ** Look at the graph above Question 5 and see where the validation scores lie for the various depths that have been assigned to the model. Does it get better with increased depth? At what point do we get our best validation score without overcomplicating our model? And remember, Occams Razor states "Among competing hypotheses, the one with the fewest assumptions should be selected."

# **Answer: ** Max depth of 3 in my opinion generalizes the unseen data best.
# At this depth the validation score is maximum. After this depth the training score keeps improving but validation score remains constant or decreases slightly.

# -----
# 
# ## Evaluating Model Performance
# In this final section of the project, you will construct a model and make a prediction on the client's feature set using an optimized model from `fit_model`.

# ### Question 7 - Grid Search
# * What is the grid search technique?
# * How it can be applied to optimize a learning algorithm?
# 
# ** Hint: ** When explaining the Grid Search technique, be sure to touch upon why it is used,  what the 'grid' entails and what the end goal of this method is. To solidify your answer, you can also give an example of a parameter in a model that can be optimized using this approach.

# **Answer: **Grid-search is a way to select the best of a family of models, parametrized by a grid of parameters. 
# These parameters called hyperparameters are not learnt by the model, but set by the user. Multiple values for these parameters are provided to the classifier and fitted, then it returns the best parameter value, which is then passed to the classifier by grid_search to improve the algorithm e.g. we can find out the best values of hyperparameters C, gamma, and kernel passed to the Kernel SVM algorithm as follows:
# 
# from sklearn.model_selection import GridSearchCV
# parameters = [{'C': [1, 10, 100, 1000], 'kernel': ['linear']},
#               {'C': [1, 10, 100, 1000], 'kernel': ['rbf'], 'gamma': [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]}]
# grid_search = GridSearchCV(estimator = classifier,
#                            param_grid = parameters,
#                            scoring = 'accuracy',
#                            cv = 10,
#                            n_jobs = -1)
# grid_search = grid_search.fit(X_train, y_train)
# best_accuracy = grid_search.best_score_
# best_parameters = grid_search.best_params_

# ### Question 8 - Cross-Validation
# 
# * What is the k-fold cross-validation training technique? 
# 
# * What benefit does this technique provide for grid search when optimizing a model?
# 
# **Hint:** When explaining the k-fold cross validation technique, be sure to touch upon what 'k' is, how the dataset is split into different parts for training and testing and the number of times it is run based on the 'k' value.
# 
# When thinking about how k-fold cross validation helps grid search, think about the main drawbacks of grid search which are hinged upon **using a particular subset of data for training or testing** and how k-fold cv could help alleviate that. You can refer to the [docs](http://scikit-learn.org/stable/modules/cross_validation.html#cross-validation) for your answer.

# **Answer: **Cross-validation is a technique for evaluating ML models by training several ML models on subsets of the available input data and evaluating them on the complementary subset of the data. In k-fold cross-validation, the original sample is randomly partitioned into k equal sized subsamples (also known as folds). Of the k subsamples, a single subsample is retained as the validation data for testing the model, and the remaining k − 1 subsamples are used as training data.
# 
# Without k-fold cross-validation, gridsearch techniques would still be using the same subset of data to train or test model, which does not provide anything new to the algorithm to learn. In other words, GridSearch will have bias for the data due to repeatedly using the same subdatasets. With k-fold, samples keep changing for train/test, and model keeps learning without any bias for the data.
# 

# ### Implementation: Fitting a Model
# Your final implementation requires that you bring everything together and train a model using the **decision tree algorithm**. To ensure that you are producing an optimized model, you will train the model using the grid search technique to optimize the `'max_depth'` parameter for the decision tree. The `'max_depth'` parameter can be thought of as how many questions the decision tree algorithm is allowed to ask about the data before making a prediction. Decision trees are part of a class of algorithms called *supervised learning algorithms*.
# 
# In addition, you will find your implementation is using `ShuffleSplit()` for an alternative form of cross-validation (see the `'cv_sets'` variable). While it is not the K-Fold cross-validation technique you describe in **Question 8**, this type of cross-validation technique is just as useful!. The `ShuffleSplit()` implementation below will create 10 (`'n_splits'`) shuffled sets, and for each shuffle, 20% (`'test_size'`) of the data will be used as the *validation set*. While you're working on your implementation, think about the contrasts and similarities it has to the K-fold cross-validation technique.
# 
# Please note that ShuffleSplit has different parameters in scikit-learn versions 0.17 and 0.18.
# For the `fit_model` function in the code cell below, you will need to implement the following:
# - Use [`DecisionTreeRegressor`](http://scikit-learn.org/stable/modules/generated/sklearn.tree.DecisionTreeRegressor.html) from `sklearn.tree` to create a decision tree regressor object.
#   - Assign this object to the `'regressor'` variable.
# - Create a dictionary for `'max_depth'` with the values from 1 to 10, and assign this to the `'params'` variable.
# - Use [`make_scorer`](http://scikit-learn.org/stable/modules/generated/sklearn.metrics.make_scorer.html) from `sklearn.metrics` to create a scoring function object.
#   - Pass the `performance_metric` function as a parameter to the object.
#   - Assign this scoring function to the `'scoring_fnc'` variable.
# - Use [`GridSearchCV`](http://scikit-learn.org/0.17/modules/generated/sklearn.grid_search.GridSearchCV.html) from `sklearn.grid_search` to create a grid search object.
#   - Pass the variables `'regressor'`, `'params'`, `'scoring_fnc'`, and `'cv_sets'` as parameters to the object. 
#   - Assign the `GridSearchCV` object to the `'grid'` variable.

# In[16]:


# Import 'make_scorer', 'DecisionTreeRegressor', and 'GridSearchCV'
from sklearn.tree import DecisionTreeRegressor
from sklearn.grid_search import GridSearchCV
from sklearn.metrics import make_scorer
from sklearn.cross_validation import ShuffleSplit

def fit_model(X, y):
    """ Performs grid search over the 'max_depth' parameter for a 
        decision tree regressor trained on the input data [X, y]. """
    
    # Create cross-validation sets from the training data
    # sklearn version 0.18: ShuffleSplit(n_splits=10, test_size=0.1, train_size=None, random_state=None)
    # sklearn versiin 0.17: ShuffleSplit(n, n_iter=10, test_size=0.1, train_size=None, random_state=None)
    cv_sets = ShuffleSplit(X.shape[0], n_iter = 10, test_size = 0.20, random_state = 8)
    #cv_sets = ShuffleSplit(X.shape[0], n_splits = 10, test_size = 0.20, random_state = 8)

    # Create a decision tree regressor object
    regressor = DecisionTreeRegressor(random_state = 8)
    regressor.fit(X, y)
    #y_pred = regressor.predict(X)
    
    # Create a dictionary for the parameter 'max_depth' with a range from 1 to 10
    params = { 'max_depth': [1,2,3,4,5,6,7,8,9,10]}

    # Transform 'performance_metric' into a scoring function using 'make_scorer' 
    scoring_fnc = make_scorer(performance_metric)

    # Create the grid search cv object --> GridSearchCV()
    # Make sure to include the right parameters in the object:
    # (estimator, param_grid, scoring, cv) which have values 'regressor', 'params', 'scoring_fnc', and 'cv_sets' respectively.
    grid = GridSearchCV(estimator = regressor,
                       param_grid = params,
                       scoring = scoring_fnc,
                       cv = cv_sets)

    # Fit the grid search object to the data to compute the optimal model
    grid = grid.fit(X, y)

    # Return the optimal model after fitting the data
    return grid.best_estimator_


# ### Making Predictions
# Once a model has been trained on a given set of data, it can now be used to make predictions on new sets of input data. In the case of a *decision tree regressor*, the model has learned *what the best questions to ask about the input data are*, and can respond with a prediction for the **target variable**. You can use these predictions to gain information about data where the value of the target variable is unknown — such as data the model was not trained on.

# ### Question 9 - Optimal Model
# 
# * What maximum depth does the optimal model have? How does this result compare to your guess in **Question 6**?  
# 
# Run the code block below to fit the decision tree regressor to the training data and produce an optimal model.

# In[17]:


# Fit the training data to the model using grid search
reg = fit_model(X_train, y_train)

# Produce the value for 'max_depth'
print("Parameter 'max_depth' is {} for the optimal model.".format(reg.get_params()['max_depth']))


# ** Hint: ** The answer comes from the output of the code snipped above.
# 
# **Answer: ** 4, which is different than the max_depth of 3 mentioned in question 6. It may be due to the fact that one is result of a visual inspection, while other is the actual calculation.

# ### Question 10 - Predicting Selling Prices
# Imagine that you were a real estate agent in the Boston area looking to use this model to help price homes owned by your clients that they wish to sell. You have collected the following information from three of your clients:
# 
# | Feature | Client 1 | Client 2 | Client 3 |
# | :---: | :---: | :---: | :---: |
# | Total number of rooms in home | 5 rooms | 4 rooms | 8 rooms |
# | Neighborhood poverty level (as %) | 17% | 32% | 3% |
# | Student-teacher ratio of nearby schools | 15-to-1 | 22-to-1 | 12-to-1 |
# 
# * What price would you recommend each client sell his/her home at? 
# * Do these prices seem reasonable given the values for the respective features? 
# 
# **Hint:** Use the statistics you calculated in the **Data Exploration** section to help justify your response.  Of the three clients, client 3 has has the biggest house, in the best public school neighborhood with the lowest poverty level; while client 2 has the smallest house, in a neighborhood with a relatively high poverty rate and not the best public schools.
# 
# Run the code block below to have your optimized model make predictions for each client's home.

# In[19]:


# Produce a matrix for client data
client_data = [[5, 17, 15], # Client 1
               [4, 32, 22], # Client 2
               [8, 3, 12]]  # Client 3

# Show predictions
for i, price in enumerate(reg.predict(client_data)):
    print("Predicted selling price for Client {}'s home: ${:,.2f}".format(i+1, price))


# **Answer: Predicted selling price for Client 1's home: $402,531.82   Predicted selling price for Client 2's home: 237,900.00  Predicted selling price for Client 3's home: 923,766.67  Price seems to be reasonable since this house has 5 bedrooms compared to average number of rooms in the Boston's houses 6.24 and the average price of $464343. Same way 2nd house has only 4 bedrooms compared to average 6, while the 3rd house has 8 bedrooms compared to average 6 in Boston.

# ### Sensitivity
# An optimal model is not necessarily a robust model. Sometimes, a model is either too complex or too simple to sufficiently generalize to new data. Sometimes, a model could use a learning algorithm that is not appropriate for the structure of the data given. Other times, the data itself could be too noisy or contain too few samples to allow a model to adequately capture the target variable — i.e., the model is underfitted. 
# 
# **Run the code cell below to run the `fit_model` function ten times with different training and testing sets to see how the prediction for a specific client changes with respect to the data it's trained on.**

# In[20]:


vs.PredictTrials(features, prices, fit_model, client_data)


# ### Question 11 - Applicability
# 
# * In a few sentences, discuss whether the constructed model should or should not be used in a real-world setting.  
# 
# **Hint:** Take a look at the range in prices as calculated in the code snippet above. Some questions to answering:
# - How relevant today is data that was collected from 1978? How important is inflation?
# - Are the features present in the data sufficient to describe a home? Do you think factors like quality of apppliances in the home, square feet of the plot area, presence of pool or not etc should factor in?
# - Is the model robust enough to make consistent predictions?
# - Would data collected in an urban city like Boston be applicable in a rural city?
# - Is it fair to judge the price of an individual home based on the characteristics of the entire neighborhood?

# **Answer: ** This model can be used as a ballpark estimate of the Boston's houses. Although data is from 1978, it still looks relevant. Inflation is quite important and the prices should also be tied to the inflation. Features present in the data are not enough for a buyer to buy the houses. Additional features like number of bathrooms should also be included. Model is robust enough to make consistent predictions. Data collected in the urban Boston will not be applicable in the rural city because features would have entirely different values there. Yes, it is fair to judge the price of an individual home based on the characteristics of entire neighborhood.

# > **Note**: Once you have completed all of the code implementations and successfully answered each question above, you may finalize your work by exporting the iPython Notebook as an HTML document. You can do this by using the menu above and navigating to  
# **File -> Download as -> HTML (.html)**. Include the finished document along with this notebook as your submission.
