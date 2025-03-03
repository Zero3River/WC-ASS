# mysql cluster

First install the Custom Resource Definition (CRD) used by MySQL Operator for Kubernetes:

```bash
kubectl apply -f k8s/mysql/deploy-crds.yaml
```

Next deploy MySQL Operator for Kubernetes, which also includes RBAC definitions as noted in the output:

```bash
kubectl apply -f k8s/mysql/deploy-operator.yaml
```

Verify that the operator is running by checking the deployment that is managing the operator inside the mysql-operator namespace, a configurable namespace defined by deploy-operator.yaml:

```bash
kubectl get deployment mysql-operator --namespace mysql-operator
```

## Deploy DB cluster

**secrets**

```bash
kubectl apply -f k8s/config/mysql-secrets.yaml
```


Use that newly created user to configure a new MySQL InnoDB Cluster. This example's InnoDBCluster definition creates three MySQL server instances and one MySQL Router instance:


```bash
kubectl apply -f k8s/mysql/deploy-db.yaml
```

Optionally observe the process by watching the innodbcluster type for the default namespace:

```bash
kubectl get innodbcluster  -n url-shortener --watch
# 也可以看看这个
kubectl get pods -n url-shortener

```
Output looks similar to this:

```bash
NAME          STATUS    ONLINE   INSTANCES   ROUTERS   AGE
mycluster     PENDING   0        3           1         10s

Until reaching ONLINE status:

NAME        STATUS   ONLINE   INSTANCES   ROUTERS   AGE
mycluster   ONLINE   3        3           1         2m6s
```

To demonstrate, this example connects with MySQL Shell to show the host name:

```bash
kubectl run --rm -it myshell -n url-shortener  --image=container-registry.oracle.com/mysql/community-operator -- mysqlsh root@mysql-cluster --sql
```

密码是mysql-secret里的sakila

**output**
```bash
If you don't see a command prompt, try pressing enter.
******

MySQL mycluster SQL> SELECT @@hostname

+-------------+
| @@hostname  |
+-------------+
| mycluster-0 |
+-------------+

```

退出是`\q`
