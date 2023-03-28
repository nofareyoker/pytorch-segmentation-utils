import numpy as np
#Evaluation metrics
def pixel_accuracy(prediction,truth):
  correct = (prediction==truth).sum().item()
  return correct/truth.numel()

def pixel_accuracy_for_class(prediction,truth,label):
  label_indices = truth == label
  correct = (prediction[label_indices] == truth[label_indices]).sum()
  return (correct/(label_indices).sum()).item()

def pixel_accuracy_all_classes(prediction,truth,n_labels):
  return np.array([pixel_accuracy_for_class(prediction,truth,label) for label in range(n_labels)])

def iou_for_class(prediction,truth,label):
  class_indices = truth == label
  intersect = (prediction[class_indices] == label).sum()
  union = class_indices.sum() + (prediction == label).sum() - intersect
  return (intersect/union).item()

def iou_all_classes(prediction,truth,n_labels):
  return np.array([iou_for_class(prediction,truth,label) for label in range(n_labels)])

def f1(prediction,truth,label):
  positive_indices = truth == label
  negative_indices = truth != label
  tp = (truth[positive_indices] == prediction[positive_indices]).sum().item()
  fp = (truth[negative_indices] != prediction[negative_indices]).sum().item()
  fn = (truth[positive_indices] != prediction[positive_indices]).sum().item()
  return (2*tp)/(2*tp + fp + fn)

def f1_all_classes(prediction,truth,n_labels):
  return np.array([f1(prediction,truth,label) for label in range(n_labels)])


class MetricManager():
  #All metric functions must take same arguments

  def __init__(self):
    self.functions = {}
    self.function_keywords = {}
    self.stats = {}

  def add_metric(self,name,function,**keywords):
    self.functions[name] = function
    self.function_keywords[name] = keywords
    self.stats[name] = np.array([])

  def crunch(self,*args):
    for name in self.functions.keys():
      result = self.functions[name](*args,**self.function_keywords[name])
      self.stats[name] = np.append(self.stats[name],result)

  def get_metric(self,name):
    return self.stats[name]