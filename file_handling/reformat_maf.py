'''
Reformats file from maf format to a sparse binary matrix

Author: Stephanie Ting
Stephanie.Ting.3@gmail.com
Written sometime in 2018

Last edited:
4/29/2024
'''

import pandas as pd
import numpy as np
from copy import deepcopy

def produce_variant_file(
    maf_input_file,
    tsv_output_file,
    key_file=None,
    is_copy_number=False,
    gene_identifier_format=None,
    gene_identifier='Hugo_Symbol',
    mutation_classification_identifier='Variant_Classification',
    sample_identifier='Tumor_Sample_Barcode',
    protein_change_identifier='Protein_Change',
    underscore_and_truncate_sample_names=False,
    variant_thres=80,
    change_thres=80,
    genes_with_all_entries=[],
    only_select_from_list=False,
    output_format='sparse_binary_matrix'):

    """
    Takes a file in maf or tsv format and outputs a sparse binary matrix or a list of samples
    that have each mutation.

    Parameters:

        maf_input_file - string - file path to the input file

        tsv_output_file - string - file path and name of desired output file

        key_file - string - path and file name of file to map genes to gene names

        gene_identifier_format - string - identifier type for genes. Must be one of the following:
            
            - 'Gene stable ID' (ex. ENSG00000284532)
            - 'Gene name' (default) (ex. MIR4723)
            - 'Gene stable ID version' (ex. ENSG00000284532.1)
            - 'Transcript stable ID' (ex. ENST00000585070)
            - 'Transcript stable ID version' (ex. ENST00000585070.1)
            
        gene_identifier - string - name of the column in file that contains gene identifiers

        mutation_classification_identifier - string - name of the column in file that contains the
            type of each variant

        sample_identifier - string - name of the column in file that contains the sample names

        protein_change_identifier - string - name of the column in file that contains the amino acid change
            information in the protein (ex. E79K)

        underscore_and_truncate_sample_names - boolean - specifically for TCGA to change the format
            of the sample names to TCGA_XX_XXXX

        variant_thres - int - lower threshold requirement for how many total variants per gene exist.
            Genes with total variants less than the variant_thres will not be included in the output file.
            With very large files, recommend higher threshold.

        change_thres - int - lower threshold requirement for how many total variants are in each variant 
            classification (ex. missense mutations) in order for that classification to be included in the
            output file. With very large files, recommend higher threshold.

        genes_with_all_entries - list of string gene names - list of gene names in which the variant and
            change threshold will be ignored

        only_select_from_list - boolean - if true will only use genes in genes_with_all_entries list and
            will not include any other genes in the final output file. Runs much faster than otherwise.

        output_format (TODO) - string - chooses whether to output a sparse binary matrix or a list of
            samples for each variant. Sparse binary matrix is much less storage efficient
    """
    
    print("Reading file...")
    d=pd.read_csv(maf_input_file, sep='\t', header=0, index_col=None, dtype=str)
    ds=d.loc[:,[gene_identifier, sample_identifier,mutation_classification_identifier, protein_change_identifier]]

    if key_file:

        key_df=pd.read_csv(key_file, sep='\t')
        key_df.set_index(gene_identifier_format, inplace=True)
        key_df=key_df['Gene name']
        key_df=key_df.drop_duplicates()
        count=set()

        #Remove gene identifier rows that don't have a corresponding gene name
        for i in ds.index:
            if not pd.isna(i):
                if not ds.loc[i, gene_identifier] in key_df.index:
                    count.add(i)
        ds.drop(labels=list(count), axis=0, inplace=True)

    sample_set=set()
    for i in ds[sample_identifier]:
        sample_set.add(i)
    sample_dict=dict(zip(list(sample_set), range(0, len(sample_set))))

    if only_select_from_list:
        print("Selecting from list of genes...")
        final_dict={}
        for gene in genes_with_all_entries:
            gene_ds=ds.loc[ds[gene_identifier]==gene]
            for i in gene_ds.index:
                sample_key=sample_dict[gene_ds.loc[i, sample_identifier]]

                protein_change=gene_ds.loc[i, protein_change_identifier]
                variant_class=gene_ds.loc[i, mutation_classification_identifier]
                
                if output_format=='sparse binary matrix':

                    if not protein_change is np.nan: 
                        if not gene+'_'+protein_change in final_dict:
                            final_dict[gene+'_'+protein_change] = [0]*len(sample_dict)
                        final_dict[gene+'_'+protein_change][sample_key]=1
                    
                    if variant_class != 'Silent': 
                        if not gene+'_Nonsilent' in final_dict:
                            final_dict[gene+'_Nonsilent'] = [0]*len(sample_dict)
                        final_dict[gene+'_Nonsilent'][sample_key]=1
            
                    if not gene+'_'+variant_class in final_dict:
                        final_dict[gene+"_"+variant_class] = [0]*len(sample_dict)
                    final_dict[gene+'_'+variant_class][sample_key]=1            
             
                    if not gene+'_MUT_All' in final_dict:
                        final_dict[gene+"_MUT_All"] = [0]*len(sample_dict)
                    final_dict[gene+'_MUT_All'][sample_key]=1            

                elif output_format=='list of samples':

                    if not protein_change is np.nan: 
                        if not gene+'_'+protein_change in final_dict:
                            final_dict[gene+'_'+protein_change] = [0]*len(sample_dict)
                        final_dict[gene+'_'+protein_change][sample_key]=1
                    
                    if variant_class != 'Silent': 
                        if not gene+'_Nonsilent' in final_dict:
                            final_dict[gene+'_Nonsilent'] = [0]*len(sample_dict)
                        final_dict[gene+'_Nonsilent'][sample_key]=1
            
                    if not gene+'_'+variant_class in final_dict:
                        final_dict[gene+"_"+variant_class] = [0]*len(sample_dict)
                    final_dict[gene+'_'+variant_class][sample_key]=1            
             
                    if not gene+'_MUT_All' in final_dict:
                        final_dict[gene+"_MUT_All"] = [0]*len(sample_dict)
                    final_dict[gene+'_MUT_All'][sample_key]=1                    

    elif is_copy_number:

        print("Creating index...")
        final_dict={}
        for gene in genes_with_all_entries:
            gene_ds=ds.loc[ds[gene_identifier]==gene]
            for i in gene_ds.index:
                sample_key=sample_dict[gene_ds.loc[i, sample_identifier]]

                variant_class=gene_ds.loc[i, mutation_classification_identifier]
                
                if output_format=='sparse binary matrix':

                    if not gene+'_'+variant_class in final_dict:
                        final_dict[gene+"_"+variant_class] = [0]*len(sample_dict)
                    final_dict[gene+'_'+variant_class][sample_key]=1            
             

                elif output_format=='list of samples':

                    if not gene+'_'+variant_class in final_dict:
                        final_dict[gene+"_"+variant_class] = [0]*len(sample_dict)
                    final_dict[gene+'_'+variant_class][sample_key]=1            
             
    else:

        print("Counting each type of variant...")
        #Keep track of how many variants per gene
        gene_variant_count={}

        for i in ds.index:
            symbol=ds.loc[i,gene_identifier]
        
            if not ds.loc[i, protein_change_identifier] is np.nan:
                variant_name=ds.loc[i, protein_change_identifier]
            
            else:
                variant_name=None
        
            if symbol in gene_variant_count:
            
                gene_variant_count[symbol]['variant'].add(variant_name)
            
                if ds.loc[i, mutation_classification_identifier] not in gene_variant_count[symbol]:
                
                    gene_variant_count[symbol][ds.loc[i,mutation_classification_identifier]]=1
                
                    gene_variant_count[symbol]['MUT_All']=1

                    if ds.loc[i, mutation_classification_identifier]!='Silent' and ('Nonsilent' not in gene_variant_count[symbol]):
                        gene_variant_count[symbol]['Nonsilent']=1
                    
                else:
                    
                    if ds.loc[i, mutation_classification_identifier]!='Silent':
                        gene_variant_count[symbol]['Nonsilent']+=1
                    
                    gene_variant_count[symbol]['MUT_All']+=1
                    gene_variant_count[symbol][ds.loc[i,mutation_classification_identifier]]+=1
        
            else:
                gene_variant_count[symbol]={}
                gene_variant_count[symbol]['variant']=set([variant_name])
                if ds.loc[i, mutation_classification_identifier]!='Silent':
                    gene_variant_count[symbol]['Nonsilent']=1
                gene_variant_count[symbol][ds.loc[i, mutation_classification_identifier]]= 1
                gene_variant_count[symbol]['MUT_All']=1


        if genes_with_all_entries==None:
            genes_with_all_entries=[]
        
        _gene_variant_count=deepcopy(gene_variant_count)
        
        print("Dropping variants under threshold...")
        for gene in _gene_variant_count:
            if key_file:
                final_gene=key_df.loc[gene]
            else:
                final_gene=gene

            if not (final_gene in genes_with_all_entries):

                for variant_type in _gene_variant_count[gene]:       
                    if variant_type == 'variant':
                        if len(_gene_variant_count[gene]['variant'])<variant_thres:                      
                            gene_variant_count[gene].pop('variant')
                            if len(gene_variant_count[gene].values())==0:
                                gene_variant_count.pop(gene)
                    else:
                        if _gene_variant_count[gene][variant_type]<change_thres:
                            gene_variant_count[gene].pop(variant_type)
                            if len(gene_variant_count[gene].values())==0:
                                gene_variant_count.pop(gene)

        final_dict={}

        print("Creating final table...")

        #Go through table line by line
        
        for gene in gene_variant_count:
            gene_ds=ds.loc[ds[gene_identifier]==gene]
            for i in gene_ds.index:
                variant_class=gene_ds.loc[i, mutation_classification_identifier]
                protein_change=gene_ds.loc[i, protein_change_identifier]
                sample_key=sample_dict[gene_ds.loc[i, sample_identifier]]
            
                if key_file:
                    final_gene = key_df.loc[gene]
                else:
                    final_gene = gene
                    
                if "variant" in gene_variant_count[gene]:
                
                    #Add to final_dict
                    if not protein_change is np.nan: 
                        if not final_gene+'_'+str(protein_change) in final_dict:
                            final_dict[final_gene+'_'+protein_change] = [0]*len(sample_dict)
                        final_dict[final_gene+'_'+protein_change][sample_key]=1
                
                if variant_class != 'Silent' and "Nonsilent" in gene_variant_count[gene]:
                    if not final_gene+'_Nonsilent' in final_dict:
                        final_dict[final_gene+'_Nonsilent'] = [0]*len(sample_dict)
                    final_dict[final_gene+'_Nonsilent'][sample_key]=1
        
                if variant_class in gene_variant_count[gene]:
                    if not final_gene+'_'+variant_class in final_dict:
                        final_dict[final_gene+"_"+variant_class] = [0]*len(sample_dict)
                    final_dict[final_gene+'_'+variant_class][sample_key]=1            
                

    print("Creating DataFrame")

    pre_table=pd.DataFrame(final_dict, index=sample_dict.keys()).T
    
    if underscore_and_truncate_sample_names:
        print("Editing sample names...")
        column_list=[]
        for i in pre_table.columns:
            column_list.append('_'.join(i.split(sep='-')[:3]))
        pre_table.columns=column_list
        
    print ("Writing to "+ tsv_output_file)
    pre_table.to_csv(tsv_output_file, sep='\t')
    return pre_table
