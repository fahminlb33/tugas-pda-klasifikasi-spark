# Tugas Crawling dan Analisis Topik Berita

Saya running script ini di local menggunakan Apache Spark di local juga.
Pastikan *environment variable* seperti `JAVA_HOME`, `SPARK_HOME` dan
lainnya sudah diatur dengan tepat agar Spark dapat dijalankan dari `pyspark`.

Selain itu saya juga menggunakan Miniconda untuk membuat *virual env*,
saya sudah commit file *environment*-nya pada file `pda-env.yml` apabila
Anda ingin mencoba menjalankan kode ini di perangkat Anda.

```bash
# membuat environment baru (pyspark, scrapy, pandas, plotly)
conda env create --file pda-env.yml
conda activate pda

# melakukan crawling
scrapy runspider uzone_spider.py

# buat dataset dalam format Parquet
python generate_dataset.py
```

Setelah dataset dibuat, proses modelling terdapat di dalam file `classify.ipynb`.
Ikuti petunjuk pada Jupyter Notebook untuk melakukan *modelling*!

## Catatan

Saya menggunakan *absolute path* untuk menyimpan hasil *scrapping* dan dataset.
Harap cek terlebih dahulu *script*-nya sebelum dieksekusi.

Versi spark: 
