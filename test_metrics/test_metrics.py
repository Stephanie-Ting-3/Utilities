import pandas as pd

def sens(tp, fn):
    return (tp/(tp+fn))

def spec(tn, fp):
    return (tn/(fp+tn))

def calculate(
        results,
        true_labels,
        what
        ):
    '''
    results - (n,1) dimensional pandas dataframe containing binary predicted labels
                labels must be numeric
    true_labels - (n,1) dimensional pandas dataframe containing binary true labels
                labels must be numeric
                
    what - list-like containing some combination of: 'sensitivity', 'specificity'
    '''
    labels=pd.concat([results, true_labels], axis=1)
    
    tp=((labels==[1,1]).sum(axis=1)==2).sum()
    
    fp=((labels==[1,0]).sum(axis=1)==2).sum()
    
    fn=((labels==[0,1]).sum(axis=1)==2).sum()
    
    tn=((labels==[0,0]).sum(axis=1)==2).sum()

    metrics=[]
    for i in what:
        if i=='sensitivity':
            metrics.append(sens(tp, fn))
        elif i=='specificity':
            metrics.append(spec(tn, fp))
        else:
            print ("Error: what must be list like containing \"sensitivity\" and/or \"specificity\"")
    return (metrics)
            
