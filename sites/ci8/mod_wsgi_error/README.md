# mod_wsgi: Truncated or oversized response headers received from daemon process

Iesterday I created a new environment for my Django application, so, like usal, I have started new *Ubuntu EC2* instance on *AWS*, I have run the *Ansible* scripts in order to configurate all the things an I have deployed last version of my code. I have loaded the login page an work well, but when I tryed to logged in I got a *500* from **Apache**.

So, I readed the `error.log` of my virtualhost and I found:

```
[Sat May 18 12:13:50.811055 2019] [wsgi:error] [pid 4430:tid 140736708159232] [client 192.168.33.1:60193] Truncated or oversized response headers received from daemon process 'django': /var/www/django/project/project/wsgi.py
```

After googling a bit is clear that this error is very generic.

In the global Apache `error.log` (located in `/var/log/apache2/error.log` for me), I found more detail:

```
[Sat May 18 12:13:50.811055 2019] [wsgi:error] [pid 4430:tid 140736708159232] [client 192.168.33.1:60193] Truncated or oversized response headers received from daemon process 'django': /var/www/django/project/project/wsgi.py
[Sat May 18 12:13:50.883186 2019] [core:notice] [pid 4428:tid 140737354034112] AH00051: child pid 4574 exit signal Segmentation fault (11), possible coredump in /etc/apache2
```

Well, this doesn't help me so I tryed to analize the problem.

The login page works, but I can't do a login. So I check some other pages and seems that many public pages works but not all.

I taked a simple view that doesn't work and I added many logs and I discovered that the last log was before a query (`MyModel.objects.get(pk=id)`).

In order to preserve the environment I replicated that in a Vagrant VM (thanks Ansible!) and, in a fresh Django project, I added this view:

```
def index(request):
    if 'query' in request.GET:
        u = User.objects.get(pk=1)

        return HttpResponse('Query performed')

    return HttpResponse('Query skipped')
```

With *SQlite* this view work fine but, when I use *PostgreSQL*, crash, so probably the problem is `psycopg2` and I confirmed my ipotesi with this code:

```
def index(request):
    if 'query' in request.GET:
        import psycopg2
        conn = psycopg2.connect("host=localhost dbname=test user=dbuser password=password")

        return HttpResponse('Query performed')

    return HttpResponse('Query skipped')
```

In order to find some more detail I changed the `LogLevel` to `debug` in my `/etc/apache2/apache2.conf`, but w/o success:

```
[Sat May 18 12:17:29.828471 2019] [authz_core:debug] [pid 4694:tid 139917057312512] mod_authz_core.c(820): [client 192.168.33.1:60222] AH01626: authorization result of Require all granted: granted
[Sat May 18 12:17:29.828772 2019] [authz_core:debug] [pid 4694:tid 139917057312512] mod_authz_core.c(820): [client 192.168.33.1:60222] AH01626: authorization result of <RequireAny>: granted
[Sat May 18 12:17:29.828881 2019] [authz_core:debug] [pid 4694:tid 139917057312512] mod_authz_core.c(820): [client 192.168.33.1:60222] AH01626: authorization result of Require all granted: granted
[Sat May 18 12:17:29.828889 2019] [authz_core:debug] [pid 4694:tid 139917057312512] mod_authz_core.c(820): [client 192.168.33.1:60222] AH01626: authorization result of <RequireAny>: granted
[Sat May 18 12:17:29.938470 2019] [wsgi:error] [pid 4694:tid 139917057312512] [client 192.168.33.1:60222] Truncated or oversized response headers received from daemon process 'django': /var/www/django/project/project/wsgi.py
[Sat May 18 12:17:29.974182 2019] [authz_core:debug] [pid 4693:tid 139917065705216] mod_authz_core.c(820): [client 192.168.33.1:60223] AH01626: authorization result of Require all granted: granted, referer: http://192.168.33.10/?query
[Sat May 18 12:17:29.974392 2019] [authz_core:debug] [pid 4693:tid 139917065705216] mod_authz_core.c(820): [client 192.168.33.1:60223] AH01626: authorization result of <RequireAny>: granted, referer: http://192.168.33.10/?query
[Sat May 18 12:17:29.974670 2019] [authz_core:debug] [pid 4693:tid 139917065705216] mod_authz_core.c(820): [client 192.168.33.1:60223] AH01626: authorization result of Require all granted: granted, referer: http://192.168.33.10/?query
[Sat May 18 12:17:29.974803 2019] [authz_core:debug] [pid 4693:tid 139917065705216] mod_authz_core.c(820): [client 192.168.33.1:60223] AH01626: authorization result of <RequireAny>: granted, referer: http://192.168.33.10/?query
[Sat May 18 12:17:30.079477 2019] [core:notice] [pid 4689:tid 139917596691392] AH00051: child pid 4835 exit signal Segmentation fault (11), possible coredump in /etc/apache2
[Sat May 18 12:17:30.079808 2019] [wsgi:info] [pid 4689:tid 139917596691392] mod_wsgi (pid=4835): Process 'django' has died, deregister and restart it.
[Sat May 18 12:17:30.080275 2019] [wsgi:info] [pid 4689:tid 139917596691392] mod_wsgi (pid=4835): Process 'django' terminated by signal 11
[Sat May 18 12:17:30.080779 2019] [wsgi:info] [pid 4689:tid 139917596691392] mod_wsgi (pid=4835): Process 'django' has been deregistered and will no longer be monitored.
[Sat May 18 12:17:30.081560 2019] [wsgi:info] [pid 4843:tid 139917596691392] mod_wsgi (pid=4843): Starting process 'django' with uid=1001, gid=1001 and threads=1.
[Sat May 18 12:17:30.082562 2019] [wsgi:info] [pid 4843:tid 139917596691392] mod_wsgi (pid=4843): Initializing Python.
[Sat May 18 12:17:30.089932 2019] [wsgi:info] [pid 4843:tid 139917596691392] mod_wsgi (pid=4843): Attach interpreter ''.
[Sat May 18 12:17:30.090366 2019] [wsgi:info] [pid 4843:tid 139917596691392] mod_wsgi (pid=4843): Adding '/var/www/django/project/' to path.
[Sat May 18 12:17:30.090838 2019] [wsgi:info] [pid 4843:tid 139917596691392] mod_wsgi (pid=4843): Adding '/var/www/django/.virtualenv/lib/python2.7/site-packages' to path.
[Sat May 18 12:17:30.091181 2019] [wsgi:info] [pid 4843:tid 139917596691392] mod_wsgi (pid=4843): Adding '/var/www/django/.virtualenv/lib/python2.7' to path.
[Sat May 18 12:17:30.091807 2019] [wsgi:debug] [pid 4843:tid 139917465523968] src/server/mod_wsgi.c(8908): mod_wsgi (pid=4843): Started thread 0 in daemon process 'django'.
[Sat May 18 12:17:30.097143 2019] [wsgi:info] [pid 4843:tid 139917465523968] mod_wsgi (pid=4843): Create interpreter 'vagrant.vm|'.
[Sat May 18 12:17:30.098289 2019] [wsgi:info] [pid 4843:tid 139917465523968] mod_wsgi (pid=4843): Adding '/var/www/django/project/' to path.
[Sat May 18 12:17:30.098649 2019] [wsgi:info] [pid 4843:tid 139917465523968] mod_wsgi (pid=4843): Adding '/var/www/django/.virtualenv/lib/python2.7/site-packages' to path.
[Sat May 18 12:17:30.099020 2019] [wsgi:info] [pid 4843:tid 139917465523968] mod_wsgi (pid=4843): Adding '/var/www/django/.virtualenv/lib/python2.7' to path.
[Sat May 18 12:17:30.099579 2019] [wsgi:info] [pid 4843:tid 139917465523968] [remote 192.168.33.1:60223] mod_wsgi (pid=4843, process='django', application='vagrant.vm|'): Loading WSGI script '/var/www/django/project/project/wsgi.py'.
[Sat May 18 12:17:30.244122 2019] [deflate:debug] [pid 4693:tid 139917065705216] mod_deflate.c(856): [client 192.168.33.1:60223] AH01384: Zlib: Compressed 13 to 21 : URL /favicon.ico, referer: http://192.168.33.10/?query
```

At this point I tried to retrieve the core dump, so I applied some configuration to **systemd**: 

```
$ sudo systemctl edit apache2
```

In the editor I wrote this:

```
[Service]
LimitCORE=infinity
```

I also added `CoreDumpDirectory /var/coredumps` in `/etc/apache2/apache2.conf`, replaced the content of `/proc/sys/kernel/core_pattern` with `/var/coredumps/core-%e-%s-%u-%g-%p-%t` and created the *coredumps* folder:

```
$ sudo mkdir -p /var/coredumps
$ sudo chmod a+w /var/coredumps
$ echo /var/coredumps/core-%e-%s-%u-%g-%p-%t > /proc/sys/kernel/core_pattern
```

I analyzed my core dump with **GDB**:

```
$ gdb apache2 /var/coredumps/core-apache2-11-1001-1001-6080-1558183433 
GNU gdb (Ubuntu 8.1-0ubuntu3) 8.1.0.20180409-git
Copyright (C) 2018 Free Software Foundation, Inc.
License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.  Type "show copying"
and "show warranty" for details.
This GDB was configured as "x86_64-linux-gnu".
Type "show configuration" for configuration details.
For bug reporting instructions, please see:
<http://www.gnu.org/software/gdb/bugs/>.
Find the GDB manual and other documentation resources online at:
<http://www.gnu.org/software/gdb/documentation/>.
For help, type "help".
Type "apropos word" to search for commands related to "word"...
Reading symbols from apache2...(no debugging symbols found)...done.
[New LWP 6080]
[New LWP 6161]
[New LWP 6162]
[New LWP 6163]
[Thread debugging using libthread_db enabled]
Using host libthread_db library "/lib/x86_64-linux-gnu/libthread_db.so.1".
Core was generated by `%{GLOBAL}         -k start'.
Program terminated with signal SIGSEGV, Segmentation fault.
#0  0x00007fdf1454cbf9 in __GI___poll (fds=0x7ffee1223230, nfds=1, timeout=-1) at ../sysdeps/unix/sysv/linux/poll.c:29
29      ../sysdeps/unix/sysv/linux/poll.c: No such file or directory.
[Current thread is 1 (Thread 0x7fdf15330bc0 (LWP 6080))]

(gdb) bt full
#0  0x00007fdf1454cbf9 in __GI___poll (fds=0x7ffee1223230, nfds=1, timeout=-1) at ../sysdeps/unix/sysv/linux/poll.c:29
        resultvar = 18446744073709551100
        sc_cancel_oldtype = 0
        sc_ret = <optimized out>
#1  0x00007fdf14a6c71a in apr_poll () from /usr/lib/x86_64-linux-gnu/libapr-1.so.0
No symbol table info available.
#2  0x00007fdf0ff165a2 in ?? () from /usr/lib/apache2/modules/mod_wsgi.so
No symbol table info available.
#3  0x00007fdf0ff17d84 in ?? () from /usr/lib/apache2/modules/mod_wsgi.so
No symbol table info available.
#4  0x0000563e685a607b in ap_run_pre_mpm ()
No symbol table info available.
#5  0x00007fdf1122d34f in ?? () from /usr/lib/apache2/modules/mod_mpm_event.so
No symbol table info available.
#6  0x0000563e685a2f3e in ap_run_mpm ()
No symbol table info available.
#7  0x0000563e6859b79b in main ()
No symbol table info available.
(gdb) 
```

Seems clear that **mod_wsgi** cause the crash when it call the [apr_poll](https://apr.apache.org/docs/apr/1.6/group__apr__poll.html#gad1d8a1ccd14952be6da5f272ca8dda76) function, but why? Unfortunately mod_wsgi was complied w/o symbols, so, in order to have many information, I compiled mod_wsgi from the source code:

```
$ sudo apt-get install apache2-dev
$ wget https://github.com/GrahamDumpleton/mod_wsgi/archive/4.5.21.tar.gz
$ tar xvfz 4.5.21.tar.gz
$ cd mod_wsgi-4.5.21/
$ ./configure
$ make
$ sudo make install
$ sudo service apache2 restart
```

I generated a new core dump and more details are available:

```
#0  0x00007fe0e9502bf9 in __GI___poll (fds=0x7fff23134e00, nfds=1, timeout=-1) at ../sysdeps/unix/sysv/linux/poll.c:29
29      ../sysdeps/unix/sysv/linux/poll.c: No such file or directory.
[Current thread is 1 (Thread 0x7fe0ea2e6bc0 (LWP 11862))]
(gdb) bt full
#0  0x00007fe0e9502bf9 in __GI___poll (fds=0x7fff23134e00, nfds=1, timeout=-1) at ../sysdeps/unix/sysv/linux/poll.c:29
        resultvar = 18446744073709551100
        sc_cancel_oldtype = 0
        sc_ret = <optimized out>
#1  0x00007fe0e9a2271a in apr_poll () from /usr/lib/x86_64-linux-gnu/libapr-1.so.0
No symbol table info available.
#2  0x00007fe0e4ecc8d2 in wsgi_daemon_main (daemon=0x7fe0ea19be70, p=0x7fe0ea2ef028) at src/server/mod_wsgi.c:9505
        buf = ""
        nbytes = 1
        i = <optimized out>
        rv = <optimized out>
        thread_rv = 1
        thread_attr = 0x7fe0ea21b840
        reaper = 0x7fe0ea21b8d0
        poll_fd = {p = 0x0, desc_type = APR_POLL_FILE, reqevents = 1, rtnevents = 0, desc = {f = 0x7fe0ea21b4d0, s = 0x7fe0ea21b4d0}, client_data = 0x7fe0ea19bd50}
        poll_count = 0
        thread_attr = <optimized out>
        reaper = <optimized out>
        i = <optimized out>
        rv = <optimized out>
        thread_rv = <optimized out>
        poll_fd = <optimized out>
        poll_count = <optimized out>
        sr__ = <optimized out>
        sr__ = <optimized out>
        sr__ = <optimized out>
        thread = <optimized out>
        sr__ = <optimized out>
        sr__ = <optimized out>
        sr__ = <optimized out>
        sr__ = <optimized out>
        buf = <optimized out>
        nbytes = <optimized out>
        sr__ = <optimized out>
        sr__ = <optimized out>
        sr__ = <optimized out>
        sr__ = <optimized out>
        sr__ = <optimized out>
        sr__ = <optimized out>
        sr__ = <optimized out>
        sr__ = <optimized out>
#3  wsgi_start_process (p=0x7fe0ea2ef028, daemon=0x7fe0ea19be70) at src/server/mod_wsgi.c:10222
        status = <optimized out>
        lr = <optimized out>
        daemon = 0x7fe0ea19be70
        i = <optimized out>
        state = <optimized out>
        entry = <optimized out>
        port = <optimized out>
        status = <optimized out>
        lr = <optimized out>
        limit = <optimized out>
        limit = <optimized out>
        limit = <optimized out>
        host = <optimized out>
        errfile = <optimized out>
        result = <optimized out>
        result = <optimized out>
        result = <optimized out>
        result = <optimized out>
        key = <optimized out>
        envvar = <optimized out>
        envvar = <optimized out>
        oldfile = <optimized out>
        p = 0x7fe0ea2ef028
        entries = <optimized out>
        sr__ = <optimized out>
        sr__ = <optimized out>
        sr__ = <optimized out>
        sr__ = <optimized out>
        sr__ = <optimized out>
        sr__ = <optimized out>
        sr__ = <optimized out>
        sr__ = <optimized out>
        sr__ = <optimized out>
        sr__ = <optimized out>
        sr__ = <optimized out>
        sr__ = <optimized out>
        sr__ = <optimized out>
        server = <optimized out>
        sr__ = <optimized out>
        sr__ = <optimized out>
        sr__ = <optimized out>
        status = <optimized out>
        lr = <optimized out>
        sr__ = <optimized out>
        sr__ = <optimized out>
        sr__ = <optimized out>
        sr__ = <optimized out>
        sr__ = <optimized out>
        sr__ = <optimized out>
        key = <optimized out>
        host = <optimized out>
        port = <optimized out>
        sr__ = <optimized out>
        limit = <optimized out>
        result = <optimized out>
        sr__ = <optimized out>
        limit = <optimized out>
        result = <optimized out>
        sr__ = <optimized out>
        limit = <optimized out>
        result = <optimized out>
        sr__ = <optimized out>
        envvar = <optimized out>
        sr__ = <optimized out>
        envvar = <optimized out>
        result = <optimized out>
        sr__ = <optimized out>
        sr__ = <optimized out>
        state = <optimized out>
        server = <optimized out>
        errfile = <optimized out>
        oldfile = <optimized out>
        sr__ = <optimized out>
        sr__ = <optimized out>
        sr__ = <optimized out>
#4  0x00007fe0e4ece0c4 in wsgi_start_daemons (p=0x7fe0ea2ef028) at src/server/mod_wsgi.c:10434
        status = <optimized out>
        entries = <optimized out>
        entry = 0x7fe0ea235028
        process = <optimized out>
        mpm_generation = 0
        i = <optimized out>
        j = 1
#5  0x000055c89679a07b in ap_run_pre_mpm ()
No symbol table info available.
#6  0x00007fe0e61e334f in ?? () from /usr/lib/apache2/modules/mod_mpm_event.so
No symbol table info available.
#7  0x000055c896796f3e in ap_run_mpm ()
No symbol table info available.
#8  0x000055c89678f79b in main ()
No symbol table info available.
```

The crash occurred in line 9505 of `src/server/mod_wsgi.c`:

```
9499    /* Block until we get a process shutdown signal. */
9500
9501    while (1) {
9502        char buf[1];
9503        apr_size_t nbytes = 1;
9504
9505        rv = apr_poll(&poll_fd, 1, &poll_count, -1);
9506        if (APR_STATUS_IS_EINTR(rv))
9507            continue;
            ....
```

Unfortunately this does not help me.

After googling a lot I found [this doc section](https://modwsgi.readthedocs.io/en/develop/user-guides/application-issues.html#ssl-shared-library-conflicts) that talk about the conflict in the shared library and I set up 2 solution to my problem:

 1. disable **mod_http2**
 2. update **psycopg2** at version 2.8 or greater

## Conclusions

The problem in **mod_wsgi** seems to be caused by the shared libraries. I have not idea about the relation with **mod_http2** but i think that the different version of **libz** in **mod_wsgi** and **_psycopg.so** can be the problem. Indeed, the problem occur with al the *psycopg* versions between *1.7.3.1* and *1.7.7* but does not occur fromn the version *2.8* or greater and this is also the first version whit *libz.so.1* instead of *ibz-a147dcb0.so.1.2.3*.

```
$ ldd /usr/lib/apache2/modules/mod_wsgi.so
        libz.so.1 => /lib/x86_64-linux-gnu/libz.so.1 (0x00007fb23d7ad000)
$ ldd /var/www/django/.virtualenv/lib/python2.7/site-packages/psycopg2/_psycopg.so | grep libz
        libz-a147dcb0.so.1.2.3 => /var/www/django/.virtualenv/lib/python2.7/site-packages/psycopg2/.libs/libz-a147dcb0.so.1.2.3 (0x00007f847bd6d000)
$ pip install psycopg2=2.7.7
$ ldd /var/www/django/.virtualenv/lib/python2.7/site-packages/psycopg2/_psycopg.so | grep libz
        libz-a147dcb0.so.1.2.3 => /var/www/django/.virtualenv/lib/python2.7/site-packages/psycopg2/.libs/libz-a147dcb0.so.1.2.3 (0x00007f847bd6d000)
$ pip install psycopg2=2.8
$ ldd /var/www/django/.virtualenv/lib/python2.7/site-packages/psycopg2/_psycopg.so
        libz.so.1 => /lib/x86_64-linux-gnu/libz.so.1 (0x00007f774ecf3000)
```

## Environmens

#### Prod

 - Ubuntu 18.04.2 LTS (GNU/Linux 4.15.0-1032-aws x86_64)
 - Apache 2.4.39
 - OpenSSL 1.1.1b
 - mod_wsgi 4.5.17
 - mod_http2 1.14.1
 - Python 2.7.15rc1
 - Django==1.9.10
 - psycopg2==2.7.3.1
 - many other libraries

#### VM

 - Ubuntu 18.04.2 LTS (GNU/Linux 4.15.0-29-generic x86_64)
 - Apache 2.4.29
 - mod_wsgi 4.5.17
 - Python 2.7.15rc1
 - Django==1.9.10
 - psycopg2==2.7.3.1
 - many other libraries

In order to use this VM you can use Ansible:
 
```
$ wget https://raw.githubusercontent.com/ciotto/boxes/master/mod_wsgi_error/Vagrantfile
$ vagrant up
$ vagrant ssh
```

You can generate the error at address [http://192.168.33.10?query](http://192.168.33.10?query).

If you want to login as django user you can do this by the Vagrant key:

```
$ wget https://raw.githubusercontent.com/mitchellh/vagrant/master/keys/vagrant
$ ssh -i vagrant django@192.168.33.10
```
