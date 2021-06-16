import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import memleak
import unittest

class TestMemleak(unittest.TestCase):
    # check if script isolates variable name correctly
    def test_isolate_variable_ActiveBusObject(self):
        self.assertEqual(memleak.IsolateVarName("var vBO = TheApplication().ActiveBusObject();"), "vBO", "Should be vBO")

    def test_isolate_variable_GetBusObject(self):
        self.assertEqual(memleak.IsolateVarName("var oBO = this.GetBusObject(\"User Preferences\");"), "oBO", "Should be oBO")

    def test_isolate_variable_GetBusComp(self):
        self.assertEqual(memleak.IsolateVarName("var oBC = oBO.GetBusComp(\"User Preferences\");"), "oBC", "Should be oBC")

    def test_isolate_variable_ParentBusComp(self):
        self.assertEqual(memleak.IsolateVarName("parentBusComp = myBusComp.ParentBusComp();"), "parentBusComp", "Should be parentBusComp")

    def test_isolate_variable_GetService(self):
        self.assertEqual(memleak.IsolateVarName("svcServerRequest  = TheApplication().GetService(\"Asynchronous Server Requests\");"), "svcServerRequest", "Should be svcServerRequest")

    def test_isolate_variable_NewPropertySet(self):
        self.assertEqual(memleak.IsolateVarName("var PS = TheApplication().NewPropertySet();"), "PS", "Should be PS")

    def test_isolate_variable_GetMVGBusComp(self):
        self.assertEqual(memleak.IsolateVarName("MvgBusComp= myBusComp.GetMVGBusComp(FieldName);"), "MvgBusComp", "Should be MvgBusComp")

    def test_isolate_variable_GetPicklistBusComp(self):
        self.assertEqual(memleak.IsolateVarName("pickBusComp = myBusComp.GetPicklistBusComp(FieldName);"), "pickBusComp", "Should be pickBusComp")

    # check if destruction order of BCs and BOs are evaluated correctly
    def test_destruction_order(self):
        test_file_name = 'test_file.csv'
        csv_file = open(test_file_name, 'a')
        test_script = "function TestDestructionOrder()\n{\ntry    \n{          \noBO1 = TheApplication().GetBusObject(\"Business Object\");\noBC1 = oBO1.GetBusComp(\"Business Component\");\noBO2 = TheApplication().GetBusObject(\"Business Object2\");\noBC2 = oBO2.GetBusComp(\"Business Component2\");\n\n}  \ncatch(e)  \n{  \nTheApplication().RaiseErrorText(e.toString());  \n}  \nfinally   \n{  \noBO1 = null;\noBC1 = null;\noBC2 = null;\noBO2 = null;\n}\n}"
        memleak.CheckOrderDestruction(test_script, csv_file, "BUSINESS SERVICE", "Test Business Service", "TestDestructionOrder")
        csv_file.close()
        with open(test_file_name) as f:
            test_file_num_of_rows = len([0 for _ in f])
        if(os.path.exists(test_file_name) and os.path.isfile(test_file_name)):
            os.remove(test_file_name)
        self.assertGreater(test_file_num_of_rows, 0, "Number of rows should be 1")

    # check if variable destruction is being evaluated correctly
    def test_check_destruction(self):
        test_script = "function TestVariablesDestruction()\n{\ntry    \n{           \nvar varDestroyed = this.ActiveBusObject();\nvar notDestroyed  = TheApplication().NewPropertySet();   \n\n}  \ncatch(e)  \n{  \nTheApplication().RaiseErrorText(e.toString());  \n}  \nfinally   \n{  \nvarDestroyed = null;  \n}\n}"
        self.assertTrue(memleak.CheckDestruction(test_script, "varDestroyed", '', 5), "Should be true")
        self.assertFalse(memleak.CheckDestruction(test_script, "notDestroyed", '', 6), "Should be false")

if __name__ == '__main__':
    unittest.main()