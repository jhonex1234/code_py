nom_ar,valor=0,0
lista=[]

while (nom_ar<=(len(letters)-1)):
    
    cleanText = re.sub('[^\w\s]', '', letters[letters.Name == letters['Name'][nom_ar]].CleanText.values[0])
        
    nom_ar=nom_ar+1
    
    #resolution art first
    search_result  = re.findall('\s*resuelve\s*articulo\s*(primero|1)\s*(\w*)', cleanText)
    # number sspd
    val_sspd=set(re.findall('\s*sspd\s(\d{14})\s', cleanText))
    #date sspd
    val_sspd_fe=set(re.findall('sspd\s*\d*\sfecha\s*(\d*\S*|\d)', cleanText))
    #expedient
    val_expedient=set(re.findall('\s(\d*\e)\s', cleanText))  
    #expedient father
    val_expedient_father=set(re.findall('radicado\spadre\s(\d{14})\s', cleanText))
    #number solve of decision 
    val_solve_decision=re.findall('\s*resuelve\s*articulo\s*(primero|1)\s*\w*\s*decision\s*(administrativa| )\s*(no|n0| )(\d*)\s', cleanText)
    #date decision
    val_decision_fe= re.findall('\s*resuelve\s*articulo\s*(primero|1)\s*\w*\s*decision\s*(administrativa| )\s*(no|n0| )\d*(\s*\d*\s\w*\s\d*\s\d*)', cleanText)
    # number_RE
    val_number_re=set(re.findall('(no|n0| )\s*(re\d*)\s', cleanText)) 
    # RE_date
    val_re_fe=re.findall('(no|n0| )\s*re\d*\s(\d{2}\s\w*\s\d{4})',cleanText)

    
    dc = {'resolucion':search_result,'sspd' : (val_sspd, val_sspd_fe),'expediente_padre' : val_expedient_father , 
          'num_decision':(val_solve_decision , val_decision_fe) , 'radicado_RE':(val_number_re , val_re_fe)}
    
    lista.append(dc)
    print('_____________________________________________________________________________doc',valor,'\n')
    print('doc->',letters['Name'][valor],' \n',dc,'\n')
    valor = valor+1
    
