import names
import random
import datetime 
import barnum
import re




class PatientRandom:
    def __init__(self,Pediatric,**kwargs):
        if Pediatric == 1:
            start_date = datetime.date(2005, 1, 1)
        else:
            start_date = datetime.date(1920, 1, 1)
        end_date = datetime.date(2020, 1, 1)   
        time_between_dates = end_date - start_date
        days_between_dates = time_between_dates.days
        random_number_of_days = random.randrange(days_between_dates)
        MaleFemale = random.randint(0, 1)
        BirthDate = start_date + datetime.timedelta(days=random_number_of_days)
        CityZip = barnum.create_city_state_zip()
        CitySlice = slice(1,2)
        ZipSlice = slice(0,1)
        x =(CityZip[CitySlice])
        y =(CityZip[ZipSlice])
        Cit = str(x).replace("\'","").replace("(","").replace(")","").replace(",","")
        ZipCod = str(y).replace("\'","").replace("(","").replace(")","").replace(",","")
        LastName = names.get_last_name()
        NaturalId = str(BirthDate).replace("-","") + str(MaleFemale) + str(random.randint(1111111,9999999))

        if MaleFemale == 0:
            FirstName = names.get_first_name(gender='male')

        if MaleFemale == 1:
            FirstName = names.get_first_name(gender='female')
        
        self.FirstName = FirstName
        self.LastName = LastName
        self.BirthDate = BirthDate
        self.Gender = MaleFemale
        self.NaturalId = NaturalId
        self.City = Cit
        self.Street = barnum.create_street()
        self.ZipCode = ZipCod

        # update properties if kwargs are passed 
        self.__dict__.update(kwargs)






#testperson = PatientRandom(Pediatric=1)
#print (testperson.__dict__)            
