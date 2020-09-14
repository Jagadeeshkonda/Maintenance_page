import boto3
import sys

lis = boto3.client('elbv2')
"""
This function is used to get the loadbalancer arn,targert group arn and listener arn
"""
def selection(product,environment):
        global lbarn
        global tgrarn
        global lisarn
        lbarn_lis = []
        response = lis.describe_load_balancers()
#through this loop we are getting and appending all the loadbalancer arn in a list
        for i in range(len(response["LoadBalancers"])):
                lbarn_lis.append(response["LoadBalancers"][i]["LoadBalancerArn"])

        tag = lis.describe_tags(ResourceArns = lbarn_lis)
        prodselec = []
        envselec = []
#through this loop we are getting and appending all the tags of the loadbalancer in a list.Also we are seperating lbs with product type
        for i in range(len(tag["TagDescriptions"])):
                for j in range(len(tag["TagDescriptions"][i]["Tags"])):
                        if tag["TagDescriptions"][i]["Tags"][j].get("Key") == "product":
                                if tag["TagDescriptions"][i]["Tags"][j].get("Value") == product:
                                        prodselec.append(tag["TagDescriptions"][i])
#here we are selecting and appending the elb arn tags by given environment
        for i in range(len(prodselec)):
                for j in range(len(prodselec[i]["Tags"])):
                        if prodselec[i]["Tags"][j].get("Key") == "environment":
                                if prodselec[i]["Tags"][j].get("Value") == environment:
                                        envselec.append(tag["TagDescriptions"][i])
# selecting the required elb arn using the elbname tag
        for i in range(len(envselec)):
                for j in range(len(envselec[i]["Tags"])):
                        if envselec[i]["Tags"][j].get("Key") == "elbname":
                                if envselec[i]["Tags"][j].get("Value") =="lendingstream.co.uk":
                                        lbarn = tag["TagDescriptions"][i]["ResourceArn"]
#describing and selecting tags of the target group. Also we are selecting the target group arn using service tag

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
#entering the maintenance mode function

        listenerArn = lisarn
        res = lis.describe_rules(ListenerArn= listenerArn)
#Iterating the rules dict to get the weight and targetgroup arn
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
#checking the mode and targertgroup arn
                                        if mode == "enable":
                                                if  trg["TargetGroupArn"] == tgrarn :
                                                        lis1 = {'TargetGroupArn': trg["TargetGroupArn"],'Weight': 1}
                                                else:
                                                        lis1 = {'TargetGroupArn': trg["TargetGroupArn"],'Weight': 0}

                                                tgp.append(lis1)
                                        if mode == "disable":
                                                if  trg["TargetGroupArn"] != tgrarn :
                                                        lis1 = {'TargetGroupArn': trg["TargetGroupArn"],'Weight': 1}
                                                else:
                                                        lis1 = {'TargetGroupArn': trg["TargetGroupArn"],'Weight': 0}
                                                tgp.append(lis1)



                                print tgp
#modifying the listeners rule
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
                                                if trg["TargetGroupArn"] == tgrarn:
                                                        lis1 = {'TargetGroupArn': trg["TargetGroupArn"],'Weight': 1}
                                                else:
                                                        lis1 = {'TargetGroupArn': trg["TargetGroupArn"],'Weight': 0}
                                                tgp.append(lis1)
                                        if mode == "disable":
                                                if  trg["TargetGroupArn"] != tgrarn :
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
