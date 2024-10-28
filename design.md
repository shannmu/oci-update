# 前置知识
[OCI 镜像格式规范](https://www.rectcircle.cn/posts/oci-image-spec)
[skopeo](https://github.com/containers/skopeo)

# OCI 镜像 format
- index.json索引menifest列表, 每个menifest代表OCI镜像的不同版本
    OCI镜像版本需要一直更新, 不能维护在latest
- menifest文件索引layers列表与config文件
    
# 动态更新的对象
- index.json
- 最新的menifest
- menifest索引的layers(更新的部分)与config

# TOOD
## 现在有什么
- 太空端: 一个手动执行的脚本 => 可以添加新的oci镜像与添加docker镜像 (原镜像都还有保存, 存储大量消耗)
- 地面端: 一个手动执行的脚本 => 获取oci镜像增量更新, 并打包

## 期望做什么
- 地面端: 可以不更新, 手动执行也可以
- 太空端: 
  - 代码定期执行/监测文件更新 => 触发脚本执行
  - 降低存储消耗(optional)
    - 地面端主动删除 => 地面端主动执行指令删除
    - 新镜像build => 触发原镜像删除
    - 其他触发机制 => 触发原镜像删除