# 数据存储

数据爬下来了怎么存也是个问题，本着不引入额外库的出发点，用的 Python 原生支持的 sqlite。数据量也不大，用这个也够了

图片在前面已经提到过，保存到本地 static 目录下，并按原始路径做目录分层


## ORM

裸操作 sqlite 还是太麻烦，搜了下 ORM，找到 peewee 这个库

大部分操作看看手册就可以搞定，这里也不多说

自己在工程里最近都在用 MongoDB，前后用了 PyMongo（最基础的 ORM），MongoKit（加了功能增强的 ORM），MongoKat（MongoKit 不更新后为了兼容新版的 fork），MongoKet（并没有这个库，是 MongoKat 也不更新后为了兼容新版自己魔改的 fork，因为没有完整场景覆盖就不拿出来吓人了），有一个 `insert_or_update` 的操作做的很爽，peewee 在 sqlite 下没有这个操作，只能是 `onConflict('replace')`，略有不爽
