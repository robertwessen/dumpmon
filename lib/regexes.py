import re

regexes = {
    'email': re.compile(r'[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}', re.I),
    #'ssn' : re.compile(r'\d{3}-?\d{2}-?\d{4}'),
    'hash32': re.compile(r'[^<A-F\d/]([A-F\d]{32})[^A-F\d]', re.I),
    'hash16': re.compile(r'[^<A-F\d/]([A-F\d]{16})[^A-F\d]', re.I), # early mySQL, others (too many FP?)
    'mysql_new': re.compile('r[\*^<A-F\d/]([A-F\d]{40})[^A-F\d]', re.I), # later mySQL
    'ntds_dit': re.compile(r'krbtgt', re.I), # weak match, testing to see what it turns up anyhow
    'shadow': re.compile(r'^root\:\$[0-9]\$', re.I), # box been rooted?
    'passwd': re.compile(r'^root\:x\:0\:0', re.I), # box been compromised?
    'FFF': re.compile(r'FBI\s*Friday', re.I),  # will need to work on this to not match CSS
    'lulz': re.compile(r'(lulzsec|antisec)', re.I),
    'cisco_hash': re.compile(r'enable\s+secret', re.I),
    'cisco_pass': re.compile(r'enable\s+password', re.I),
    'google_api': re.compile(r'\W(AIza.{35})'),
    'aws_access_key': re.compile(r'(?<![A-Z0-9])[A-Z0-9]{20}(?![A-Z0-9])', re.I), # testing AWS access key regex
    'honeypot': re.compile(r'<dionaea\.capture>', re.I),
    'pgp_private': re.compile(r'BEGIN PGP PRIVATE', re.I),
    'ssh_private': re.compile(r'BEGIN RSA PRIVATE', re.I),
    'db_keywords': [
		re.compile(r'((customers?|email|users?|members?|acc(?:oun)?ts?)([-_|/\s]?(address|name|id[^")a-zA-Z0-9_]|[-_:|/\\])))', re.I),
        re.compile(r'((\W?pass(wor)?d|hash)[\s|:])', re.I),
        re.compile(r'((\btarget|\bsite)\s*?:?\s*?(([a-z][\w-]+:/{1,3})?([-\w\s_/]+\.)*[\w=/?%]+))', re.I),  # very basic URL check - may be improved later
        re.compile(r'(my\s?sql[^i_\.]|sql\s*server)', re.I),
        re.compile(r'((host|target)[-_\s]+ip:)', re.I),
        re.compile(r'(data[-_\s]*base|\Wdb)', re.I),  # added the non-word char before db.. we'll see if that helps
        re.compile(r'(table\s*?:)', re.I),
        re.compile(r'((available|current)\s*(databases?|dbs?)\W)', re.I),
        re.compile(r'(hacked\s*by)', re.I)
    ],
	# I was hoping to not have to make a blacklist, but it looks like I don't really have a choice
    'blacklist': [ 
		re.compile(r'(select\s+.*?from|join|declare\s+.*?\s+as\s+|update.*?set|insert.*?into)', re.I),  # SQL
        re.compile(r'(define\(.*?\)|require_once\(.*?\))', re.I),  # PHP
        re.compile(r'(function.*?\(.*?\))', re.I),
        re.compile(r'(Configuration(\.Factory|\s*file))', re.I),
        re.compile(r'((border|background)-color)', re.I),  # Basic CSS (Will need to be improved)
        re.compile(r'(Traceback \(most recent call last\))', re.I),
        re.compile(r'(java\.(util|lang|io))', re.I),
        re.compile(r'(sqlserver\.jdbc)', re.I)
    ],
    # The banlist is the list of regexes that are found in crash reports
    'banlist': [
        re.compile(r'faf\.fa\.proxies', re.I),
        re.compile(r'Technic Launcher is starting', re.I),
        re.compile(r'OTL logfile created on', re.I),
        re.compile(r'RO Game Client crashed!', re.I),
        re.compile(r'Selecting PSO2 Directory', re.I),
        re.compile(r'TDSS Rootkit', re.I),
        re.compile(r'SysInfoCrashReporterKey', re.I),
        re.compile(r'Current OS Full name: ', re.I),
        re.compile(r'Multi Theft Auto: ', re.I),
        re.compile(r'Initializing cgroup subsys cpuset', re.I),
        re.compile(r'Init vk network', re.I),
        re.compile(r'MediaTomb UPnP Server', re.I)
    ]
}
