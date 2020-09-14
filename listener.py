import boto3
import sys

lis = boto3.client('elbv2')
"""
res1 = lis.describe_load_balancers(Names=['testbalancer'],)
elbarn = res1["LoadBalancers"][0]["LoadBalancerArn"]
response = lis.describe_target_groups(LoadBalancerArn= elbarn)
res2 = lis.describe_listeners(LoadBalancerArn = elbarn)
lisarn =  res2["Listeners"][0]["ListenerArn"]
"""
def selection(product,environment):
        global lbarn
        global tgrarn
        global lisarn
        lbarn_lis = []
        response = lis.describe_load_balancers()
        for i in range(len(response["LoadBalancers"])):
                lbarn_lis.append(response["LoadBalancers"][i]["LoadBalancerArn"])

        tag = lis.describe_tags(ResourceArns = lbarn_lis)
        prodselec = []
        envselec = []
        for i in range(len(tag["TagDescriptions"])):
                for j in range(len(tag["TagDescriptions"][i]["Tags"])):
                        if tag["TagDescriptions"][i]["Tags"][j].get("Key") == "product":
                                if tag["TagDescriptions"][i]["Tags"][j].get("Value") == product:
                                        prodselec.append(tag["TagDescriptions"][i])

        for i in range(len(prodselec)):
                for j in range(len(prodselec[i]["Tags"])):
                        if prodselec[i]["Tags"][j].get("Key") == "environment":
                                if prodselec[i]["Tags"][j].get("Value") == environment:
                                        envselec.append(tag["TagDescriptions"][i])

        for i in range(len(envselec)):
                for j in range(len(envselec[i]["Tags"])):
                        if envselec[i]["Tags"][j].get("Key") == "elbname":
                                if envselec[i]["Tags"][j].get("Value") =="lendingstream.co.uk":
                                        lbarn = tag["TagDescriptions"][i]["ResourceArn"]


        trg = lis.describe_target_groups(LoadBalancerArn = lbarn)
        trarnlis = []
        for i in range(len(trg["TargetGroups"])):
                trarnlis.append(trg["TargetGroups"][i]["TargetGroupArn"])

        tag1 = lis.describe_tags(ResourceArns = trarnlis)
        for i in range(len(tag1["TagDescriptions"])):
                for j in range(len(tag1["TagDescriptions"][i]["Tags"])):
                        if tag1["TagDescriptions"][i]["Tags"][j].get("Key") == "service":
                                                        if tag1["TagDescriptions"][i]["Tags"][j].get("Value") == "maintenance":
                                                                tgrarn = tag1["TagDescriptions"][i]["ResourceArn"]

        print "loadbalancer arn...." + lbarn
        print "targetgrp arn......." + tgrarn
        lbarn = lbarn
        tgrarn = tgrarn
        res2 = lis.describe_listeners(LoadBalancerArn = lbarn)
        lisarn =  res2["Listeners"][0]["ListenerArn"]

#lbarn = lbarn
#tgrarn = tgrarn
def maintenance_mode(tgrarn,lisarn,mode):
        """
        for cnt in range(len(response["TargetGroups"])):
                if  response["TargetGroups"][cnt]["TargetType"] == "lambda":
                        tgrarn = response["TargetGroups"][cnt]["TargetGroupArn"]
        """

        #print tgrarn

        listenerArn = lisarn
        res = lis.describe_rules(ListenerArn= listenerArn)
        for i in range(len(res["Rules"])):
                isdefault = str(res["Rules"][i]["IsDefault"])
                if isdefault == "False":
                        rulearn = res["Rules"][i]["RuleArn"]
                        for j in range(len(res["Rules"][i]["Actions"])):
                                targarn = []
                                weight = []
                                tgp = []
                                for k in range(len(res["Rules"][i]["Actions"][j]["ForwardConfig"]["TargetGroups"])):
                                        targarn.append(res["Rules"][i]["Actions"][j]["ForwardConfig"]["TargetGroups"][k]["TargetGroupArn"])
                                        weight.append(res["Rules"][i]["Actions"][j]["ForwardConfig"]["TargetGroups"][k]["Weight"])
                                        trg = res["Rules"][i]["Actions"][j]["ForwardConfig"]["TargetGroups"][k]
                                        if mode == "enable":
                                                if trg["Weight"] == 0 and trg["TargetGroupArn"] == tgrarn :
                                                        lis1 = {'TargetGroupArn': trg["TargetGroupArn"],'Weight': 1}
                                                else:
                                                        lis1 = {'TargetGroupArn': trg["TargetGroupArn"],'Weight': 0}
                                                tgp.append(lis1)
                                        if mode == "disable":
                                                if trg["Weight"] == 0 and trg["TargetGroupArn"] != tgrarn :
                                                        lis1 = {'TargetGroupArn': trg["TargetGroupArn"],'Weight': 1}
                                                else:
                                                        lis1 = {'TargetGroupArn': trg["TargetGroupArn"],'Weight': 0}
                                                tgp.append(lis1)



                                print tgp

                                modlis = lis.modify_rule(
                                RuleArn= rulearn,
                                Conditions=[],
                                Actions=[{
                                        'Type': 'forward',
                                        'ForwardConfig': {'TargetGroups': tgp}
                                        }])

                else:
                        for j in range(len(res["Rules"][i]["Actions"])):
                                targarn = []
                                weight = []
                                tgp = []
                                for k in range(len(res["Rules"][i]["Actions"][j]["ForwardConfig"]["TargetGroups"])):
                                        targarn.append(res["Rules"][i]["Actions"][j]["ForwardConfig"]["TargetGroups"][k]["TargetGroupArn"])
                                        weight.append(res["Rules"][i]["Actions"][j]["ForwardConfig"]["TargetGroups"][k]["Weight"])
                                        trg = res["Rules"][i]["Actions"][j]["ForwardConfig"]["TargetGroups"][k]
                                        if mode == "enable":
                                                if trg["Weight"] == 0 and trg["TargetGroupArn"] == tgrarn:
                                                        lis1 = {'TargetGroupArn': trg["TargetGroupArn"],'Weight': 1}
                                                else:
                                                        lis1 = {'TargetGroupArn': trg["TargetGroupArn"],'Weight': 0}
                                                tgp.append(lis1)
                                        if mode == "disable":
                                                if trg["Weight"] == 0 and trg["TargetGroupArn"] != tgrarn :
                                                        lis1 = {'TargetGroupArn': trg["TargetGroupArn"],'Weight': 1}
                                                else:
                                                        lis1 = {'TargetGroupArn': trg["TargetGroupArn"],'Weight': 0}
                                                tgp.append(lis1)
                                print tgp
                                modlis = lis.modify_listener(
                                ListenerArn= listenerArn ,
                                DefaultActions=[{
                                        'Type': 'forward',
                                        'ForwardConfig':{'TargetGroups': tgp}
                                        }])





if __name__ == '__main__':

        selection(product = sys.argv[1],environment = sys.argv[2])
        print tgrarn
        print lbarn
        maintenance_mode(tgrarn = tgrarn,lisarn = lisarn,mode = sys.argv[3])

print "pass"
