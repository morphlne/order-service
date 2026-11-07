FROM redis:alpine

COPY users.acl /etc/redis/users.acl
RUN chown redis:redis /etc/redis/users.acl && chmod 600 /etc/redis/users.acl

CMD ["redis-server", "--aclfile", "/etc/redis/users.acl", "--appendonly", "yes"]
