package com.mountain.controller;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.FSDataInputStream;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.security.UserGroupInformation;
import org.springframework.web.bind.annotation.RestController;

/**
 * @author: kejiefu
 * @create: 2023-10-10 11:01
 **/
@RestController
public class HDFSReadTest3Controller {

    public static void main(String[] args) {
        try {
            // 设置Hadoop配置
            Configuration conf = new Configuration();
            conf.set("fs.defaultFS", "hdfs://192.168.110.26:9000");

            // 设置要使用的用户
            String userName = "hadoop";
            UserGroupInformation ugi = UserGroupInformation.createRemoteUser(userName);

            // 在特权模式下执行HDFS操作
            ugi.doAs((java.security.PrivilegedExceptionAction<Void>) () -> {
                try {
                    // 获取文件系统
                    FileSystem fs = FileSystem.get(conf);

                    // 指定要读取的文件路径
                    Path filePath = new Path("/user/hadoop/example.txt");

                    // 打开文件输入流
                    FSDataInputStream inputStream = fs.open(filePath);

                    // 读取文件内容
                    byte[] buffer = new byte[1024];
                    int bytesRead;
                    StringBuilder fileContentBuilder = new StringBuilder();

                    while ((bytesRead = inputStream.read(buffer)) != -1) {
                        // 将读取的字节追加到字符串构建器中
                        fileContentBuilder.append(new String(buffer, 0, bytesRead));
                    }

                    // 将字符串构建器转换为最终的文件内容字符串
                    String fileContent = fileContentBuilder.toString();

                    // 关闭流
                    inputStream.close();

                    System.out.println("File content: " + fileContent);
                } catch (Exception e) {
                    e.printStackTrace();
                }
                return null;
            });
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
