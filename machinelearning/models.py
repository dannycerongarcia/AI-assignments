import nn

class PerceptronModel(object):
    def __init__(self, dimensions):
        """
        Initialize a new Perceptron instance.

        A perceptron classifies data points as either belonging to a particular
        class (+1) or not (-1). `dimensions` is the dimensionality of the data.
        For example, dimensions=2 would mean that the perceptron must classify
        2D points.
        """
        self.w = nn.Parameter(1, dimensions)

    def get_weights(self):
        """
        Return a Parameter instance with the current weights of the perceptron.
        """
        return self.w

    def run(self, x):
        """
        Calculates the score assigned by the perceptron to a data point x.

        Inputs:
            x: a node with shape (1 x dimensions)
        Returns: a node containing a single number (the score)
        """
        "*** YOUR CODE HERE ***"
        # using computing the dot product over the default weights with the values from the dataset
        return nn.DotProduct(self.get_weights(),x)

    def get_prediction(self, x):
        """
        Calculates the predicted class for a single data point `x`.

        Returns: 1 or -1
        """
        "*** YOUR CODE HERE ***"
        # call the runfunction to get the dot product values and then converting the values to a scalar
        prediction = nn.as_scalar(self.run(x))
        if(prediction >=0):
            return 1
        else:
            return -1

    def train(self, dataset):
        """
        Train the perceptron until convergence.
        """
        "*** YOUR CODE HERE ***"
        batch_size = 1
        check = True
        # it should loop untill the value converges?
        while check:
            check = False
            temp = self.get_weights()
            # gergular singal iteration, maybe i can use the other function
            for x , y_star in dataset.iterate_once(batch_size):
                y = self.get_prediction(x)
                # if the predicted value is the same at current weight do nothing else update
                # default weight vector
                if y == nn.as_scalar(y_star):
                    continue
                nn.Parameter.update(self.get_weights(),x,nn.as_scalar(y_star))
                check = True
            # keep looping until value converges
            if temp != self.get_weights():
                check = True


class RegressionModel(object):
    """
    A neural network model for approximating a function that maps from real
    numbers to real numbers. The network should be sufficiently large to be able
    to approximate sin(x) on the interval [-2pi, 2pi] to reasonable precision.
    """
    def __init__(self):
        # Initialize your model parameters here
        "*** YOUR CODE HERE ***"
        # We'll use the ReLU operation for our non-linearity
        self.w_1 = nn.Parameter(1,205)
        self.b_1 = nn.Parameter(1,205)
        self.w_2 = nn.Parameter(205,1)
        self.b_2 = nn.Parameter(1,1)

    def run(self, x):
        """
        Runs the model for a batch of examples.

        Inputs:
            x: a node with shape (batch_size x 1)
        Returns:
            A node with shape (batch_size x 1) containing predicted y-values
        """
        "*** YOUR CODE HERE ***"

        # normal linear gression stuff
        xw_1 = nn.Linear(x, self.w_1)
        # rectifying linear unit nonlinearity 
        lp1 = nn.ReLU(nn.AddBias(xw_1,self.b_1))
        # 
        xw_2 = nn.Linear(lp1,self.w_2)
        # returning predicted y-values
        predicted_y =  nn.AddBias(xw_2,self.b_2)
        return predicted_y

    def get_loss(self, x, y):
        """
        Computes the loss for a batch of examples.

        Inputs:
            x: a node with shape (batch_size x 1)
            y: a node with shape (batch_size x 1), containing the true y-values
                to be used for training
        Returns: a loss node
        """
        "*** YOUR CODE HERE ***"
        return nn.SquareLoss(self.run(x),y)
        

    def train(self, dataset):
        """
        Trains the model.
        """
        "*** YOUR CODE HERE ***"
        batch_size = 1
        multiplier = -.001
        loss = 0
        while (1):
            for x , y in dataset.iterate_once(batch_size):
                loss = self.get_loss(x,y)
                grad1,grad2,grad3,grad4  = nn.gradients(loss, [self.w_1, self.w_2,self.b_1,self.b_2])
                self.w_1.update(grad1,multiplier)
                self.w_2.update(grad2,multiplier)
                self.b_1.update(grad3,multiplier)
                self.b_2.update(grad4,multiplier)
            if nn.as_scalar(loss) < 0.02:
                break    

class DigitClassificationModel(object):
    """
    A model for handwritten digit classification using the MNIST dataset.

    Each handwritten digit is a 28x28 pixel grayscale image, which is flattened
    into a 784-dimensional vector for the purposes of this model. Each entry in
    the vector is a floating point number between 0 and 1.

    The goal is to sort each digit into one of 10 classes (number 0 through 9).

    (See RegressionModel for more information about the APIs of different
    methods here. We recommend that you implement the RegressionModel before
    working on this part of the project.)
    """
    def __init__(self):
        # Initialize your model parameters here
        "*** YOUR CODE HERE ***"

        # 748x100 the bigger the higher the accurarcy
        self.w_1 = nn.Parameter(784,100)
        self.b_1 = nn.Parameter(1,  100)
        self.w_2 = nn.Parameter(100, 10)
        self.b_2 = nn.Parameter(1,   10)
    def run(self, x):
        """
        Runs the model for a batch of examples.

        Your model should predict a node with shape (batch_size x 10),
        containing scores. Higher scores correspond to greater probability of
        the image belonging to a particular class.

        Inputs:
            x: a node with shape (batch_size x 784)
        Output:
            A node with shape (batch_size x 10) containing predicted scores
                (also called logits)
        """
        "*** YOUR CODE HERE ***"
        xw_1 = nn.Linear(x, self.w_1)
        # rectifying linear unit nonlinearity 
        lp1 = nn.ReLU(nn.AddBias(xw_1,self.b_1))
        # 
        xw_2 = nn.Linear(lp1,self.w_2)
        # returning predicted y-values
        predicted_y =  nn.AddBias(xw_2,self.b_2)
        return predicted_y

    def get_loss(self, x, y):
        """
        Computes the loss for a batch of examples.

        The correct labels `y` are represented as a node with shape
        (batch_size x 10). Each row is a one-hot vector encoding the correct
        digit class (0-9).

        Inputs:
            x: a node with shape (batch_size x 784)
            y: a node with shape (batch_size x 10)
        Returns: a loss node
        """
        "*** YOUR CODE HERE ***"
        # using SoftmaxLoss instead of square loss
        return nn.SoftmaxLoss(self.run(x),y)

    def train(self, dataset):
        """
        Trains the model.
        """
        "*** YOUR CODE HERE ***"
        # epochs round time depends on the bathc size
        # this means update weight after seen 40 trained data
        batch_size = 40
        
        # when we increase the batch size we need also increase the learning rate
        # this means the amount of steps skipped or taken
        multiplier = -.1
        loss = 0
        while (1):
            for x , y in dataset.iterate_once(batch_size):
                loss = self.get_loss(x,y)
                grad1,grad2,grad3,grad4  = nn.gradients(loss, [self.w_1, self.w_2,self.b_1,self.b_2])
                self.w_1.update(grad1,multiplier)
                self.w_2.update(grad2,multiplier)
                self.b_1.update(grad3,multiplier)
                self.b_2.update(grad4,multiplier)
            if dataset.get_validation_accuracy() >= .97 or dataset.epoch >= 5:
                break    

class LanguageIDModel(object):
    """
    A model for language identification at a single-word granularity.

    (See RegressionModel for more information about the APIs of different
    methods here. We recommend that you implement the RegressionModel before
    working on this part of the project.)
    """
    def __init__(self):
        # Our dataset contains words from five different languages, and the
        # combined alphabets of the five languages contain a total of 47 unique
        # characters.
        # You can refer to self.num_chars or len(self.languages) in your code
        self.num_chars = 47
        self.languages = ["English", "Spanish", "Finnish", "Dutch", "Polish"]

        # Initialize your model parameters here
        "*** YOUR CODE HERE ***"
        self.w_1 = nn.Parameter(47,100)
        self.b_1 = nn.Parameter(1,  100)
        self.w_2 = nn.Parameter(100, 100)

        self.w_e = nn.Parameter(100,5)        
        self.b = nn.Parameter(1,   5)
    def run(self, xs):
        """
        Runs the model for a batch of examples.

        Although words have different lengths, our data processing guarantees
        that within a single batch, all words will be of the same length (L).

        Here `xs` will be a list of length L. Each element of `xs` will be a
        node with shape (batch_size x self.num_chars), where every row in the
        array is a one-hot vector encoding of a character. For example, if we
        have a batch of 8 three-letter words where the last word is "cat", then
        xs[1] will be a node that contains a 1 at position (7, 0). Here the
        index 7 reflects the fact that "cat" is the last word in the batch, and
        the index 0 reflects the fact that the letter "a" is the inital (0th)
        letter of our combined alphabet for this task.

        Your model should use a Recurrent Neural Network to summarize the list
        `xs` into a single node of shape (batch_size x hidden_size), for your
        choice of hidden_size. It should then calculate a node of shape
        (batch_size x 5) containing scores, where higher scores correspond to
        greater probability of the word originating from a particular language.

        Inputs:
            xs: a list with L elements (one per character), where each element
                is a node with shape (batch_size x self.num_chars)
        Returns:
            A node with shape (batch_size x 5) containing predicted scores
                (also called logits)
        """
        "*** YOUR CODE HERE ***"
        h = nn.Linear(xs[0],self.w_1)
        
        for x in xs[1:]:
            
            h = nn.Add(nn.Linear(x,self.w_1),nn.Linear(nn.ReLU(nn.AddBias(h,self.b_1)),self.w_2))            
        z = nn.Linear(h,self.w_e)
        
        return nn.AddBias(z,self.b)

    def get_loss(self, xs, y):
        """
        Computes the loss for a batch of examples.

        The correct labels `y` are represented as a node with shape
        (batch_size x 5). Each row is a one-hot vector encoding the correct
        language.

        Inputs:
            xs: a list with L elements (one per character), where each element
                is a node with shape (batch_size x self.num_chars)
            y: a node with shape (batch_size x 5)
        Returns: a loss node
        """
        "*** YOUR CODE HERE ***"
        return nn.SoftmaxLoss(self.run(xs),y)

    def train(self, dataset):
        """
        Trains the model.
        """
        "*** YOUR CODE HERE ***"
        batch_size = 40
        
        # when we increase the batch size we need also increase the learning rate
        # this means the amount of steps skipped or taken
        multiplier = -.1
        loss = 0
         
        while (1):
            for x , y in dataset.iterate_once(batch_size):
                loss = self.get_loss(x,y)
                grad1,grad2,grad3,grad4 = nn.gradients(loss, [self.w_1, self.w_2,self.w_e,self.b])
                self.w_1.update(grad1,multiplier)
                self.w_2.update(grad2,multiplier)
                self.w_e.update(grad3,multiplier)
                self.b.update(grad4,multiplier)
            if dataset.get_validation_accuracy() >= .83 or dataset.epoch > 20:
                break
