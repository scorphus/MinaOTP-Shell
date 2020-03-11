#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : since 2018-02-06 02:26
# @Author  : Gin (gin.lance.inside@hotmail.com)
# @Link    :
# @Disc    : add remove show and list totp tokens in the terminal

import argparse
import datetime
import json
import os
import os.path
import pyotp


# global variable
OID_LEN = 6
ISSUER_LEN = 16
REMARK_LEN = 16
OTP_LEN = 16
JSON_URL = os.path.expanduser("~") + os.sep + ".mina.json"


# load tokens from json file
def load_json():
    with open(JSON_URL, "r") as f:
        if os.path.getsize(JSON_URL):
            return json.load(f)
        else:
            raise Warning


# update token to json file
def upd_json(data):
    with open(JSON_URL, "w") as f:
        json.dump(data, f, sort_keys=True, indent=4, separators=(",", ":"))


# show expiry
def print_expiry():
    sec = datetime.datetime.now().second
    sharp_c = sec % 30
    expired_time = 30 - sharp_c
    print("expires after: {}s".format(expired_time))


# print a line
def print_line(oid, issuer, remark, otp, fillchar=" "):
    print(
        oid.center(OID_LEN, fillchar),
        issuer.center(ISSUER_LEN, fillchar),
        remark.center(REMARK_LEN, fillchar),
        otp.center(OTP_LEN, fillchar),
    )


# print the header
def print_header():
    print_line("OID", "ISSUER", "REMARK", "OTP", fillchar="=")


# generate OTP for a token
def gen_otp(token):
    return pyotp.TOTP(token["secret"]).now()


# print a token
def print_token(oid, token):
    print_line(str(oid), token["issuer"], token["remark"], gen_otp(token))


# load tokens from JSON file
def load_tokens():
    try:
        return load_json()
    except IOError:
        print("ERROR: there is no .mina.json file")
    except Warning:
        print("WARNING: there is no any otp tokens in the .mina.json file.")


# list all tokens
def list_tokens():
    tokens = load_tokens()
    if tokens:
        print_header()
        for oid, token in enumerate(tokens):
            print_token(oid, token)
        print_expiry()


# show a token on-time
def show(oid):
    tokens = load_tokens()
    if tokens:
        print_header()
        print_token(oid, tokens[int(oid)])
        print_expiry()


# add a new token
def add(otp):
    try:
        tokens = load_json()
    except IOError:
        print("ERROR: there is no .mina.json file")
    except Warning:
        tokens = []
        tokens.append(otp)
        upd_json(tokens)
    else:
        tokens.append(otp)
        upd_json(tokens)


# remove a token
def remove(oid):
    tokens = load_tokens()
    if tokens:
        tokens.pop(int(oid))
        upd_json(tokens)


# import from a local json file
def import_from(file_path):
    tokens = load_tokens()
    if tokens:
        try:
            append_tokens = load_json(file_path)
        except IOError:
            print("ERROR: " + file_path + " is not a file!")
        except Warning:
            print("WARNING: there is no any otp tokens in the file!")
        else:
            tokens = tokens + append_tokens
            upd_json(tokens)


# the main function to control the script
def main():
    # Define the basic_parser and subparsers
    _desc = "MinaOTP is a two-factor authentication tool that runs in the terminal"
    basic_parser = argparse.ArgumentParser(description=_desc)
    subparsers = basic_parser.add_subparsers(dest="command", help="Available commands")

    # Subparser for the list command
    subparsers.add_parser("list", help="List all tokens.")

    # Subparser for the add command
    add_parser = subparsers.add_parser("add", help="Add a new token.")
    # OTP optional arguments
    add_parser.add_argument("--secret", required=True, help="Secret info to generate otp object.")
    add_parser.add_argument("--issuer", required=True, help="Issuer info about new otp object.")
    add_parser.add_argument("--remark", required=True, help="Remark info about new otp object.")

    # Subparser for the remove command
    remove_parser = subparsers.add_parser("remove", help="Remove a token.")
    remove_parser.add_argument("oid", help="oid of the token")

    # Subparser for the show command
    show_parser = subparsers.add_parser("show", help="Show a token on-time")
    show_parser.add_argument("oid", help="oid of the token")

    # Subparser for the import command
    import_parser = subparsers.add_parser("import", help="Import tokens from a local json file")
    import_parser.add_argument("file_path", help="path of the local json file")

    # handle the args input by user
    args = basic_parser.parse_args()
    # convert arguments to dict
    arguments = vars(args)
    command = arguments.pop("command")

    if command == "list":
        list_tokens()
    if command == "add":
        otp = {"secret": args.secret, "issuer": args.issuer, "remark": args.remark}
        add(otp)
    if command == "remove":
        target_oid = args.oid
        remove(target_oid)
    if command == "show":
        target_oid = args.oid
        show(target_oid)
    if command == "import":
        file_path = args.file_path
        import_from(file_path)


if __name__ == "__main__":
    main()
