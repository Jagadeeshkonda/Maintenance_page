import boto3
import sys

lis = boto3.client('elbv2')
res1 = lis.describe_load_balancers(Names=['testbalancer'],)
elbarn = res1["LoadBalancers"][0]["LoadBalancerArn"]
response = lis.describe_target_groups(LoadBalancerArn= elbarn)
res2 = lis.describe_listeners(LoadBalancerArn = elbarn)
lisarn =  res2["Listeners"][0]["ListenerArn"]
def maintenance_mode():
        for cnt in range(len(response["TargetGroups"])):
                if  response["TargetGroups"][cnt]["TargetType"] == "lambda":
                        tgrarn = response["TargetGroups"][cnt]["TargetGroupArn"]


        print tgrarn

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
                                        if trg["Weight"] == 0 and trg["TargetGroupArn"] == tgrarn :
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
                                        if trg["Weight"] == 0 and trg["TargetGroupArn"] == tgrarn:
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



def maintenance_disable():
        for cnt in range(len(response["TargetGroups"])):
                if  response["TargetGroups"][cnt]["TargetType"] == "lambda":
                        tgrarn = response["TargetGroups"][cnt]["TargetGroupArn"]


        print tgrarn

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
                                        if trg["Weight"] == 0 and trg["TargetGroupArn"] != tgrarn:
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
        if sys.argv[1] == "enable":
                maintenance_mode()
        if sys.argv[1] == "disable":
                maintenance_disable()
