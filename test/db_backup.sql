PGDMP      :                |           HabitTrackerdb    16.2    16.2     �           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            �           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            �           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            �           1262    16397    HabitTrackerdb    DATABASE     �   CREATE DATABASE "HabitTrackerdb" WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'Russian_Russia.1251';
     DROP DATABASE "HabitTrackerdb";
                postgres    false            �            1259    16432    alembic_version    TABLE     X   CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);
 #   DROP TABLE public.alembic_version;
       public         heap    postgres    false            �            1259    16445    complete    TABLE     �   CREATE TABLE public.complete (
    id integer NOT NULL,
    habit_id integer NOT NULL,
    complete_date date NOT NULL,
    user_id integer NOT NULL
);
    DROP TABLE public.complete;
       public         heap    postgres    false            �            1259    16444    complete_id_seq    SEQUENCE     �   CREATE SEQUENCE public.complete_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 &   DROP SEQUENCE public.complete_id_seq;
       public          postgres    false    221            �           0    0    complete_id_seq    SEQUENCE OWNED BY     C   ALTER SEQUENCE public.complete_id_seq OWNED BY public.complete.id;
          public          postgres    false    220            �            1259    16414    habits    TABLE     8  CREATE TABLE public.habits (
    id integer NOT NULL,
    title character varying(200) DEFAULT NULL::character varying,
    description character varying(200) DEFAULT NULL::character varying,
    priority integer,
    complete boolean,
    owner_id integer,
    creation_date date,
    days_of_week integer[]
);
    DROP TABLE public.habits;
       public         heap    postgres    false            �            1259    16413    todos_id_seq    SEQUENCE     �   CREATE SEQUENCE public.todos_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 #   DROP SEQUENCE public.todos_id_seq;
       public          postgres    false    218            �           0    0    todos_id_seq    SEQUENCE OWNED BY     >   ALTER SEQUENCE public.todos_id_seq OWNED BY public.habits.id;
          public          postgres    false    217            �            1259    16399    users    TABLE     �  CREATE TABLE public.users (
    id integer NOT NULL,
    email character varying(200) DEFAULT NULL::character varying,
    username character varying(45) DEFAULT NULL::character varying,
    first_name character varying(45) DEFAULT NULL::character varying,
    last_name character varying(45) DEFAULT NULL::character varying,
    hashed_password character varying(200) DEFAULT NULL::character varying,
    is_active boolean
);
    DROP TABLE public.users;
       public         heap    postgres    false            �            1259    16398    users_id_seq    SEQUENCE     �   CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 #   DROP SEQUENCE public.users_id_seq;
       public          postgres    false    216            �           0    0    users_id_seq    SEQUENCE OWNED BY     =   ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;
          public          postgres    false    215            1           2604    16448    complete id    DEFAULT     j   ALTER TABLE ONLY public.complete ALTER COLUMN id SET DEFAULT nextval('public.complete_id_seq'::regclass);
 :   ALTER TABLE public.complete ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    220    221    221            .           2604    16417 	   habits id    DEFAULT     e   ALTER TABLE ONLY public.habits ALTER COLUMN id SET DEFAULT nextval('public.todos_id_seq'::regclass);
 8   ALTER TABLE public.habits ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    217    218    218            (           2604    16402    users id    DEFAULT     d   ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);
 7   ALTER TABLE public.users ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    215    216    216            �          0    16432    alembic_version 
   TABLE DATA           6   COPY public.alembic_version (version_num) FROM stdin;
    public          postgres    false    219   �"       �          0    16445    complete 
   TABLE DATA           H   COPY public.complete (id, habit_id, complete_date, user_id) FROM stdin;
    public          postgres    false    221   �"       �          0    16414    habits 
   TABLE DATA           s   COPY public.habits (id, title, description, priority, complete, owner_id, creation_date, days_of_week) FROM stdin;
    public          postgres    false    218   @#       �          0    16399    users 
   TABLE DATA           g   COPY public.users (id, email, username, first_name, last_name, hashed_password, is_active) FROM stdin;
    public          postgres    false    216   K$       �           0    0    complete_id_seq    SEQUENCE SET     >   SELECT pg_catalog.setval('public.complete_id_seq', 31, true);
          public          postgres    false    220            �           0    0    todos_id_seq    SEQUENCE SET     ;   SELECT pg_catalog.setval('public.todos_id_seq', 17, true);
          public          postgres    false    217            �           0    0    users_id_seq    SEQUENCE SET     :   SELECT pg_catalog.setval('public.users_id_seq', 5, true);
          public          postgres    false    215            7           2606    16436 #   alembic_version alembic_version_pkc 
   CONSTRAINT     j   ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);
 M   ALTER TABLE ONLY public.alembic_version DROP CONSTRAINT alembic_version_pkc;
       public            postgres    false    219            9           2606    16450    complete complete_pkey 
   CONSTRAINT     T   ALTER TABLE ONLY public.complete
    ADD CONSTRAINT complete_pkey PRIMARY KEY (id);
 @   ALTER TABLE ONLY public.complete DROP CONSTRAINT complete_pkey;
       public            postgres    false    221            5           2606    16421    habits todos_pkey 
   CONSTRAINT     O   ALTER TABLE ONLY public.habits
    ADD CONSTRAINT todos_pkey PRIMARY KEY (id);
 ;   ALTER TABLE ONLY public.habits DROP CONSTRAINT todos_pkey;
       public            postgres    false    218            3           2606    16412    users users_pkey 
   CONSTRAINT     N   ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);
 :   ALTER TABLE ONLY public.users DROP CONSTRAINT users_pkey;
       public            postgres    false    216            ;           2606    16451    complete fk_habit_id    FK CONSTRAINT     �   ALTER TABLE ONLY public.complete
    ADD CONSTRAINT fk_habit_id FOREIGN KEY (habit_id) REFERENCES public.habits(id) ON DELETE CASCADE;
 >   ALTER TABLE ONLY public.complete DROP CONSTRAINT fk_habit_id;
       public          postgres    false    218    221    4661            <           2606    16461    complete fk_user_id    FK CONSTRAINT     �   ALTER TABLE ONLY public.complete
    ADD CONSTRAINT fk_user_id FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE NOT VALID;
 =   ALTER TABLE ONLY public.complete DROP CONSTRAINT fk_user_id;
       public          postgres    false    216    4659    221            :           2606    16422    habits todos_owner_id_fkey    FK CONSTRAINT     z   ALTER TABLE ONLY public.habits
    ADD CONSTRAINT todos_owner_id_fkey FOREIGN KEY (owner_id) REFERENCES public.users(id);
 D   ALTER TABLE ONLY public.habits DROP CONSTRAINT todos_owner_id_fkey;
       public          postgres    false    216    4659    218            �      x��4�44N21HKJ2����� (��      �   S   x�]���0���%�c��?GENn��~ٖ�z4ͦ)60/�,Q�����;�ĸ9�ؗ$�iɀ�E���t>�Yb$������#o      �   �   x�m��J�0��'Oѝ��4iZ�rf!">�l�v��Sa�"C)�]�0�V�����7È:H~.�s���B���D;�8Ŭ�ҝ)���H��nY �����6�0vU��w�S�����k�����d,�$N'q�^�+��l`9�r�@�5eC�?���r`
�Ӎt��ƽ����������}��L�H����%�����-(�fB�'�Hд������Ҷ�GP)��+����Fd�[ȗp�,�%�HO��2ƾ <7l       �   T  x�m�Ɏ�PE���A&�]�80)��� >ez�����M�6!7U9�87�¿��u�~�RA_L \D��{��ˈaG�T��]�4���h�8`s����$�ӑ�Z
>�+�u�qT�Y	L�h|���D�`Y�3�zq��H騔�0�MT��Ҋ�`��F�Ċq �j.&��zFw�`�e���+�%y�)��W{�+-��P�R,j�c���l�m��"t����۳����q�������:-���`d�m���9W�_̻ܖ�6�e��-\C�����`��o8p���jD/�z�lً�ZA^�Q�jX�d�����x��A���H��0d��     