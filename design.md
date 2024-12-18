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
  - 代码定期执行/监测文件更新(optional) => 触发脚本执行
  - 降低存储消耗(optional)
    - 地面端主动删除 => 地面端主动执行指令删除
    - 新镜像build => 触发原镜像删除
    - 其他触发机制 => 触发原镜像删除


## 代码怎么用
### 地面
```=shell
# 使用Dockerfile build镜像
docker build . -t oci-test:v1

# 使用skopeo转化 docker image => OCI image
skopeo copy docker-daemon:oci-test:v1 oci:/path/to/oci-dir:oci-test:v1 (注意使用绝对路径)

# !!!修改Dockerfile

# 使用Dockerfile build镜像
docker build . -t oci-test:v2

# 使用skopeo转化 docker image => OCI image
skopeo copy docker-daemon:oci-test:v2 oci:/path/to/oci-dir:oci-test:v2 (注意使用绝对路径, 和上面一致)

# 使用station.py (!!! 在 /path/to/oci-dir 的根目录下执行)
python /path/to/station.py --path . (这里会生成一个diff.tar.gz => 将它mv出来)

```

### 太空
```=shell
# 默认太空中的/path/to/oci-dir是有oci-test:v1的
# 可以创建一个文件夹用于放置太空端的oci-test
# skopeo copy docker-daemon:oci-test:v1 oci:/path/to/space/oci-dir:oci-test:v1 (注意使用绝对路径)


# 卫星数据上注

# 使用diff.tar.gz更新OCI镜像
# tag参数: 地面上最新的是多少就用多少
# NOTE: docker images中的oci-test image的tag永远是latest => 这样可以减少docker image的存储 + 可以使用oci image随时备份
python space.py --oci_image_root /path/to/space/oci-dir/ --tag v2 --diff_tar_path /path/to/diff.tar.gz --image_name oci-test

# 查看docker images => 发现多了oci-test:latest
docker images


```