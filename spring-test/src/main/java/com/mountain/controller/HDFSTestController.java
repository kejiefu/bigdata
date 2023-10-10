package com.mountain.controller;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IOUtils;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.SequenceFile;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.io.compress.BZip2Codec;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.io.IOException;
import java.net.URI;

/**
 * @author: kejiefu
 * @create: 2023-10-10 11:01
 **/
@RestController
public class HDFSTestController {

    //模拟数据源；数组中一个元素表示一个文件的内容
    private static final String[] DATA = {
            "The Apache Hadoop software library is a framework that allows for the distributed processing of large data sets across clusters of computers using simple programming models.",
            "It is designed to scale up from single servers to thousands of machines, each offering local computation and storage.",
            "Rather than rely on hardware to deliver high-availability, the library itself is designed to detect and handle failures at the application layer",
            "o delivering a highly-available service on top of a cluster of computers, each of which may be prone to failures.",
            "Hadoop Common: The common utilities that support the other Hadoop modules."
    };

    @RequestMapping("/test")
    public void test() throws IOException {
        //输出路径：要生成的SequenceFile文件名
        String uri = "hdfs://192.168.110.26:9000/writeSequenceFile";

        Configuration conf = new Configuration();
        FileSystem fs = FileSystem.get(URI.create(uri), conf);
        //向HDFS上的此SequenceFile文件写数据
        Path path = new Path(uri);

        //因为SequenceFile每个record是键值对的
        //指定key类型
        IntWritable key = new IntWritable(); //key数字 -> int -> IntWritable
        //指定value类型
        Text value = new Text();//value -> String -> Text

        //创建向SequenceFile文件写入数据时的一些选项
        //要写入的SequenceFile的路径
        SequenceFile.Writer.Option pathOption = SequenceFile.Writer.file(path);
        //record的key类型选项
        SequenceFile.Writer.Option keyOption = SequenceFile.Writer.keyClass(IntWritable.class);
        //record的value类型选项
        SequenceFile.Writer.Option valueOption = SequenceFile.Writer.valueClass(Text.class);
        //SequenceFile压缩方式：NONE | RECORD | BLOCK三选一
        //方案一：RECORD、不指定压缩算法
//        SequenceFile.Writer.Option compressOption   = SequenceFile.Writer.compression(SequenceFile.CompressionType.RECORD);
//        SequenceFile.Writer writer = SequenceFile.createWriter(conf, pathOption, keyOption, valueOption, compressOption);

        //方案二：BLOCK、不指定压缩算法
//        SequenceFile.Writer.Option compressOption   = SequenceFile.Writer.compression(SequenceFile.CompressionType.BLOCK);
//        SequenceFile.Writer writer = SequenceFile.createWriter(conf, pathOption, keyOption, valueOption, compressOption);

        //方案三：使用BLOCK、压缩算法BZip2Codec；压缩耗时间
        //再加压缩算法
        BZip2Codec codec = new BZip2Codec();
        codec.setConf(conf);
        SequenceFile.Writer.Option compressAlgorithm = SequenceFile.Writer.compression(SequenceFile.CompressionType.RECORD, codec);
        //创建写数据的Writer实例
        SequenceFile.Writer writer = SequenceFile.createWriter(conf, pathOption, keyOption, valueOption, compressAlgorithm);

        for (int i = 0; i < 100000; i++) {
            //分别设置key、value值
            key.set(100000 - i);
            value.set(DATA[i % DATA.length]); //%取模 3 % 3 = 0;
            System.out.printf("[%s]\t%s\t%s\n", writer.getLength(), key, value);
            //在SequenceFile末尾追加内容
            writer.append(key, value);
        }
        //关闭流
        IOUtils.closeStream(writer);
    }

}
