音乐、电影数据的排序打分模型说明[10.142.57.28]：

测试整体流程说明：
根目录：/search/odin/zql/asso_cloud_test
测试结果：/search/odin/zql/asso_cloud_test/asso_knowledge_src/testset/result.txt
测试的指标在：/search/odin/zql/asso_cloud_test/debug/stat.txt
测试动作，在debug目录下执行：./asso_test --gtest_filter=SA_Unittest.FileCases
测试电影/音乐切换，修改文件：./zql/asso_cloud_test/asso_knowledge_src/samrt_asso_unittest.cpp
td::ifstream f("../asso_knowledge_src/testset/file_testdata.txt");  //电影测试
std::ifstream f("../asso_knowledge_src/testset/music_testdata.txt");    //音乐测试
然后到debug目录里面make重新编译一下执行测试动作
数据更新：每次执行update的sh脚本后，三元组数据被更新，要把knowledgeData那个文件夹拷过来
查看指标：首选命中率、首选命中前缀率、前三选命中率、前三选命中前缀率、所有候选命中率、所有候选命中前缀率
结果文件result.txt说明：
前三列是测试数据，第一列是上文，第二列是测试集给的标签，第三列是用户数据的下一个上屏词，第四列是代码预测出来的结果，主要看第四列的排序，是根据打分来的

元组打分说明：
根路径：/work/generateTupleData[=/search/odin/tanglianrui/asso_knowledge_src_bak/generateTupleData]
电影数据相关：./movie
getMovieFromDouban/ 包含了从豆瓣爬取正在热映和即将上映的电影详细信息[每日定时任务]
tuple_score/        包含了对于给定