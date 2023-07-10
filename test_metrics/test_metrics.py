import pandas as pd

def _sens(tp, fn):
    return (tp/(tp+fn))

def _spec(tn, fp):
    return (tn/(fp+tn))

def _acc(tp, tn, total_predictions):
    return ((tp+tn)/total_predictions)

def calculate(
        results,
        true_labels,
        what
        ):

    '''
    results - 1d list-like containing binary predicted results
    true_labels - 1d list-like containing true labels                
    what - list-like containing some combination of: 'sensitivity', 'specificity', 'accuracy'
    '''
    labels=pd.DataFrame({"results":results, "true_labels":true_labels})
    
    #Match positive and negative patterns
    tp=((labels==[1,1]).sum(axis=1)==2).sum()
    
    fp=((labels==[1,0]).sum(axis=1)==2).sum()
    
    fn=((labels==[0,1]).sum(axis=1)==2).sum()
    
    tn=((labels==[0,0]).sum(axis=1)==2).sum()

    #Calculate multiple metrics
    metrics=[]
    for i in what:
        if i=='sensitivity':
            metrics.append(_sens(tp, fn))
        elif i=='specificity':
            metrics.append(_spec(tn, fp))
        elif i=='accuracy':
            metrics.append(_acc(tp, tn, len(true_labels)))
        else:
            print ("Error: what must be list-like containing \"sensitivity\", \"accuracy\" and/or \"specificity\"")
    return (metrics)
            
