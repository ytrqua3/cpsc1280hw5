import unittest
import uuid
import os
import shutil
import subprocess
import stat
import re

def asciify(input_String):
    output = ""
    for i in range(len(input_String)):
        if (input_String[i] >= "A" and input_String[i] <="Z") or \
           (input_String[i] >= "a" and input_String[i] <="z") or \
           (input_String[i] >= "0" and input_String[i] <="9") or \
           input_String[i] == " " or input_String[i] == "." or input_String[i] == "," :
           output += input_String[i]
    return output
def remove_quotes(old_string):
    return old_string.replace("\"","")

class Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        
        set_of_tests = {"part1" : {"fut" : "script5_1.sh", 
                                   "aux" :["high_tech_gdp_revenue.csv",
                                           "high_tech_gdp_revenue_copy.csv"]},
                        "part2" : {"fut" : "script5_2a.sh",
                                   "aux" : ["Tree_Species.csv", "expected5_2a_1.ref",
                                            "expected5_2a_2.ref", "expected5_2a_3.ref"]},
                        "part3" : {"fut" : "script5_2b.sh",
                                   "aux" : ["Tree_Species.csv","expected5_2b.ref"]},
                        "part4" : {"fut" : "script5_2c.sh",
                                   "aux" : ["Tree_Species.csv","expected5_2c.ref"]},
                        "part5" : {"fut" : "script5_3.sh",
                                   "aux" : ["wines_SPA.csv"]}}
        cls.tests = set_of_tests
        
        #check shell
        cls.shell = "/usr/bin/bash"
        cls.assertTrue(os.path.isfile(cls.shell), "/usr/bin/bash not found." + 
           "Operating System may not be correct. Consider using Cloud 9")
        
        #Create temp directory
        uidString = str(uuid.uuid4()) 
        cls.test_directory = "/tmp/Assignment5_"+uidString;
        os.mkdir(cls.test_directory)
        
        
        for test in cls.tests:
            #copy scripts
            shutil.copy(cls.tests[test]["fut"], cls.test_directory)
            #copy other files
            for file in cls.tests[test]["aux"] :
                shutil.copy(file, cls.test_directory)
        os.chdir(cls.test_directory)
        print("Test running in directory:" + cls.test_directory)
            
    @classmethod
    def tearDownClass(cls):
        #remove data files, as they are large
        #and will take up too much space when the test
        #is run multiple times.
        for tests in cls.tests:
            for file in cls.tests[tests]["aux"]:
                if os.path.isfile(file):
                    os.remove(file)
                pass
    

    def test_script5_1(self):
        test_file = self.tests["part1"]["fut"]
        aux1 = self.tests["part1"]["aux"][0]
        aux2 = self.tests["part1"]["aux"][1]
        print(f"running {test_file}")
        
        self.assertTrue(os.path.isfile(test_file), "Script not found")
        
        testParameters = { "test1": { "Param" : [aux1,"Other .*"], "expected": 
            'Other computer and related services,891,"1,008","1,110","1,335","1,397","1,527","1,664","1,785","1,777","1,912","2,228","2,302","2,338","2,343","2,488","2,558","2,738","3,196","3,247","3,606","3,625","3,955","4,416","4,830","5,200"'+"\n"+ 
            'Other services,468,670,595,676,719,749,864,953,"1,009","1,215","1,416","1,470","1,385","1,474","1,531","1,581","1,794","1,825","1,715","1,577","1,771","2,001","1,991","2,403","2,872"'},
                           "test2": { "Param" : [aux2,"Other .*"], "expected": 
            'Other computer and related services,891,"1,008","1,110","1,335","1,397","1,527","1,664","1,785","1,777","1,912","2,228","2,302","2,338","2,343","2,488","2,558","2,738","3,196","3,247","3,606","3,625","3,955","4,416","4,830","5,200"'+"\n"+ 
            'Other services,468,670,595,676,719,749,864,953,"1,009","1,215","1,416","1,470","1,385","1,474","1,531","1,581","1,794","1,825","1,715","1,577","1,771","2,001","1,991","2,403","2,872"'},
                           "test3": { "Param" : [aux2,"^Software"], "expected":
            'Software publishing,116,242,236,265,363,421,546,679,879,995,849,833,653,719,792,854,946,"1,034","1,059",997,"1,032","1,122","1,248","1,367","1,450"'},
                           "test4": { "Param" : [aux1,"^Software"], "expected":
            'Software publishing,116,242,236,265,363,421,546,679,879,995,849,833,653,719,792,854,946,"1,034","1,059",997,"1,032","1,122","1,248","1,367","1,450"'},}

        for para in testParameters:
            current = testParameters[para]          
            cpi = subprocess.run([self.shell, test_file, current["Param"][0], current["Param"][1]], \
                                 timeout=10,capture_output=True, text=True)
            print(f"Testing: {self.shell} {test_file} {current['Param'][0]} \"{current['Param'][1]}\"")
            print("stdout:")
            print(cpi.stdout)
            print("\nstderr:")
            print(cpi.stderr)
            output = cpi.stdout.strip()
            self.assertTrue(re.match(current["expected"], output),
                            f"Output incorrected, expected: \n" + \
                            current["expected"]+f"\nOutput: \n{output}")
        print("Test Passed")
        return
    def test_script5_2a(self):
        test_file = self.tests["part2"]["fut"]
        aux = self.tests["part2"]["aux"][0]
        expected = [self.tests["part2"]["aux"][1],self.tests["part2"]["aux"][2],self.tests["part2"]["aux"][3]]
        print(f"running {test_file}")
        self.assertTrue(os.path.isfile(test_file), "Script not found")
        
        testParameters = { "test1": { "Param" : [aux,"DALLAS [^,]*", "Wildlife snag"],
                                      "expected" : expected[0]},
                            "test2" : { "Param" : [aux,"BAY [^,]*", "Pinus [^,]*"],
                                      "expected" : expected[1]},
                            "test3" : { "Param" : [aux,"QUADRA ST", "Quercus garryana"],
                                      "expected" : expected[2]}}
        for para in testParameters:
            current = testParameters[para]          
            cpi = subprocess.run([self.shell, test_file, current["Param"][0], current["Param"][1],current["Param"][2]], \
                                 timeout=10,capture_output=True, text=True)
            print(f"Testing: {self.shell} {test_file} {current['Param'][0]} \"{current['Param'][1]}\" \"{current['Param'][2]}\"")
            print("stdout:")
            print(cpi.stdout)
            print("\nstderr:")
            print(cpi.stderr)
            output = cpi.stdout.strip()
            expectedText = ""
            with open(current["expected"]) as expected_result:
                expectedText = expected_result.read().strip()
            self.assertTrue(re.match(expectedText, output),
                            f"Output incorrect.  Please check output manually, too long to display here.")
        print("Test Passed")
        return

    def test_script5_2b(self):
        test_file = self.tests["part3"]["fut"]
        aux = self.tests["part3"]["aux"][0]
        expected = self.tests["part3"]["aux"][1]
        print(f"running {test_file}")
        self.assertTrue(os.path.isfile(test_file), "Script not found")
        
        testParameters = { "test1": { "Param" : [aux],
                                      "expected" : expected}}
        for para in testParameters:
            current = testParameters[para]          
            cpi = subprocess.run([self.shell, test_file, current["Param"][0]], \
                                 timeout=10,capture_output=True, text=True)
            print(f"Testing: {self.shell} {test_file} {current['Param'][0]}")
            print("stdout:")
            print(cpi.stdout)
            print("\nstderr:")
            print(cpi.stderr)
            output = cpi.stdout.strip()
            expectedText = ""
            with open(current["expected"]) as expected_result:
                expectedText = expected_result.read().strip()
            self.assertTrue(re.match(expectedText, output),
                            f"Output incorrect.  Please check output manually, too long to display here.")
        print("Test Passed")
        return
        
    def test_script5_2c(self):
        test_file = self.tests["part4"]["fut"]
        aux = self.tests["part4"]["aux"][0]
        expected = self.tests["part4"]["aux"][1]
        print(f"running {test_file}")
        self.assertTrue(os.path.isfile(test_file), "Script not found")
        
        testParameters = { "test1": { "Param" : [aux],
                                      "expected" : expected}}
        for para in testParameters:
            current = testParameters[para]          
            cpi = subprocess.run([self.shell, test_file, current["Param"][0]], \
                                 timeout=10,capture_output=True, text=True)
            print(f"Testing: {self.shell} {test_file} {current['Param'][0]}")
            print("stdout:")
            print(cpi.stdout)
            print("\nstderr:")
            print(cpi.stderr)
            output = cpi.stdout.strip()
            expectedText = ""
            with open(current["expected"]) as expected_result:
                expectedText = expected_result.read().strip()
            self.assertTrue(re.match(expectedText, output),
                            f"Output incorrect.  Please check output manually, too long to display here.")
        print("Test Passed")
        return
    def test_script5_3(self):
        test_file = self.tests["part5"]["fut"]
        aux = self.tests["part5"]["aux"][0]
        print(f"Testing {test_file}")
        self.assertTrue(os.path.isfile(test_file), "Script not found")
        self.assertTrue(os.path.isfile(aux), "Datafile not found")
        
        tests = [{"winery" :"Emilio Moro"},
                 {"winery" :"Bodegas Mauro"}]
        winery_idx = 0
        rating_idx = 3
        year_idx = 2
        
        ref_file = open(aux,"r")
        heading = ref_file.readline()
        data = ref_file.readlines()
        ref_file.close()
    
        results = []
        for test in tests:
            record = {}
            ratings = []
            for row in data:
                fields = row.split(",")
                if remove_quotes(fields[winery_idx]) == test["winery"]:
                    ratings.append(float(fields[rating_idx]))
            
            record.update({"max" : max(ratings)})
            max_rating = max(ratings)
            
            years = []
            for row in data:
                fields = row.split(",")
                
                if remove_quotes(fields[winery_idx]) == test["winery"] and \
                    fields[rating_idx] == str(max_rating):
                    years.append(int(remove_quotes(fields[year_idx])))
            years.sort(reverse=True)
            year_list = list(set(years))
            year_list.sort(reverse=True)
            
            record.update({"years" : year_list})
            results.append(record)
        print(results)    
        
        #run student code
        for k in range(len(tests)):
            test = tests[k]
            print(f"Test case winery = {test['winery']}")
            print(f"Expected max = {results[k]['max']}")
            
            cpi = cpi = subprocess.run(["/usr/bin/bash", test_file,
                                        aux,test["winery"]], timeout=5,capture_output=True, text=True)
            print("stderr")
            print(cpi.stderr)
            student_data = cpi.stdout.strip().split("\n")
            print(student_data[0])
            self.assertTrue(float(student_data[0])==results[k]["max"], "Maximum rating is incorrect")
            self.assertTrue(len(student_data[1:])==len(results[k]["years"]), "Different number of years found")
            years = results[k]["years"]
            for l in range(len(years)):
                self.assertTrue(years[l] == float(student_data[l+1]),"Incorect year found:" + str(student_data[l+1]))
        
        
        print("Test Passed")
            

if __name__ == '__main__':
    unittest.main()        