'''
Created on 14/07/2015

@author: hgvasqueza
'''
class Verhoeff(object):    
    mul = [[0,1,2,3,4,5,6,7,8,9],
    [1,2,3,4,0,6,7,8,9,5],
    [2,3,4,0,1,7,8,9,5,6],
    [3,4,0,1,2,8,9,5,6,7],
    [4,0,1,2,3,9,5,6,7,8],
    [5,9,8,7,6,0,4,3,2,1],
    [6,5,9,8,7,1,0,4,3,2],
    [7,6,5,9,8,2,1,0,4,3],
    [8,7,6,5,9,3,2,1,0,4],
    [9,8,7,6,5,4,3,2,1,0],] 
    
    per = [[0,1,2,3,4,5,6,7,8,9],
    [1,5,7,6,2,8,3,0,9,4],
    [5,8,0,3,7,9,6,1,4,2],
    [8,9,1,6,0,4,3,5,2,7],
    [9,4,5,3,1,2,6,8,7,0],
    [4,2,8,6,5,7,3,9,0,1],
    [2,7,9,3,8,0,6,4,1,5],
    [7,0,4,6,9,1,3,2,5,8],]
    
    inv = [0,4,3,2,1,5,6,7,8,9]
    
    def get(self,num):    
        ck = 0
        num = str(num)
        num_length = len(num)
        i = num_length-1        
        while i >= 0:        
            ck = self.mul[ck][self.per[(num_length-i) % 8][int(num[i])]]
            i = i - 1                                         
        return self.inv[ck];   
        
#test = Verhoeff()
#print test.get(1503)
class AllegedRC4(object):
    def sprintf(self, formato, *objects):
        return formato % tuple(objects)

    def swap(self,state,x,y):    
        z = state[x]
        state[x] = state[y] 
        state[y] = z
        return state
    
    def encode(self,msg, key, mode='hex'):    
        state = []
        for i in range (0,256): 
            state.append( i )
         
            
        x = 0
        y = 0
        i1= 0 
        i2= 0
        
        key_length = len(key);
       
        
        for i in range(0,256):        
            i2 = (ord(key[i1])+state[i]+i2) % 256
            self.swap(state,i,i2)            
            i1 = (i1+1) % key_length                        
        
        msg_length = len(msg)
        msg_hex = "";
        msg_aux = "";
        for i in range(0,msg_length):        
            x = (x + 1) % 256
            y = (state[x] + y) % 256
            self.swap(state,x,y)            
            
            xi = (state[x] + state[y]) % 256            
            r = ord(msg[i]) ^ state[xi]
          
            msg_aux = msg_aux + chr(r)                
            msg_hex += self.sprintf("%02X",r)
        
        if mode=="hex":
            return msg_hex
        else:
            return msg_aux

#test = AllegedRC4()
#print test.encode("HolaMundo", "1234")
class CodigoControlV7 (object):
    def generar(self, numautorizacion, numfactura, nitcliente, fecha, monto, clave):    
        numfactura = self.appendVerhoeff(numfactura, 2)            
        nitcliente = self.appendVerhoeff(nitcliente, 2)                        
        fecha = self.appendVerhoeff(fecha, 2)                
        monto = self.appendVerhoeff(monto, 2)                
        
        suma = long(numfactura) + long(nitcliente) + long(fecha) + long(monto)
        suma = self.appendVerhoeff(suma, 5)        
        suma = str(suma)
         
        dv = suma[len(suma)-5::]
                
        cads = [str(numautorizacion), numfactura, nitcliente, fecha, monto]        
                
        msg = ""
        p = 0
        for i in range(0,5):                                                            
            msg += cads[i] + clave[p:(p+1+int(dv[i]))]                
            p += (1 + int(dv[i]))              
                
        allegedRC4 = AllegedRC4()      
        codif = allegedRC4.encode(msg, clave+dv)
        st = 0
        sp = [0,0,0,0,0]
        codif_length = len(codif)
        for i in range (0,codif_length):        
            st += ord(codif[i])
            sp[i%5] += ord(codif[i])
        stt = 0
        for i in range (0,5):
            stt += (int)((st * sp[i]) / (1 + int(dv[i])))
               
        separar = allegedRC4.encode(self.base64(stt), clave+dv)        
        aux_separar = ""
        separar_length = len(separar)
        for i in xrange (separar_length):
            aux_separar += separar[i]
            if (i % 2) & (i < (separar_length-1)) :
                aux_separar += "-"                                    
        return aux_separar 
            
    def base64(self,n):    
        d = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 
        'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J',
        'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',     
        'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 
        'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 
        'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 
        'y', 'z', '+', '/']
              
        c = 1
        r = ""
        while c > 0:        
            c = (int)(n / 64)
            r = d[n%64] + r
            n = c        
        return r    
    
    def appendVerhoeff(self,n, c):
        verhoeff = Verhoeff()
        aux_n = str(n)

        while c > 0:    
            aux_n += str(verhoeff.get(aux_n))
            c -= 1                       
        return aux_n