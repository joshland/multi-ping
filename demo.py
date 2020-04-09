#!/usr/bin/env python

"""
Copyright 2017 Pani Networks Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

"""

# A small demo, which demonstrates how to use MultiPing

from multiping import MultiPing
from multiping import multi_ping

if __name__ == "__main__":
    # A list of addresses and names, which should be pinged.
    addrs = ["8.8.8.8", "cnn.com", "127.0.0.1", "youtube.com",
             "2001:4860:4860::8888"]
    #addrs = ["127.0.0.1", "10.11.1.5","10.12.1.1"]
    mp = MultiPing(addrs)

    ##
    ## Demo Basic Usage
    ##
    print("Round: 0")
    print(" [Ping]")
    mp.send()

    # First attempt: keep recv time very, to show the staggered responses.
    print(" Receive() Waiting Replies.......")
    responses, no_responses = mp.receive(0.01)

    complete = len(responses.keys()) == len(addrs)
    if complete:
        print("   received responses:  %s" % list(responses.keys()))
        print('--- Round Complete ---')
        print('')
    else:
        pending = list(responses.keys())
        print("   received responses:  %s" % pending)
        print("   no responses so far: %s" % no_responses)
        print(" Try Receive() Again.......")
        # By now we should have received responses from the others as well
        responses, no_responses = mp.receive(0.1)
        complete = (len(pending) + len(responses.keys())) == len(addrs)
        if complete:
            print("   received responses:  %s" % list(responses.keys()))
            print('--- Round Complete ---')
        else:
            print("   received responses:  %s" % list(responses.keys()))
            print("   still no responses:  %s" % no_responses)
            print("")
        pass
    print('')

    # Sometimes ICMP packets can get lost. It's easy to retry (re-send the
    # ping) to those hosts that haven't responded, yet. Send can be called
    # multiple times and will result in pings to be resent to those addresses
    # from which we have not heard back, yet. Here we try three pings max.
    print("Round 1: (3 Attempts)")
    mp = MultiPing(addrs)
    pending = []
    for i in range(3):
        print(" [Ping]")
        mp.send()

        print(" Receive() Waiting Replies.......")
        responses, no_response = mp.receive(0.01)
        pending += list(responses.keys())
        complete = len(pending) == len(addrs)

        print("    received responses:     %s" % list(responses.keys()))
        if complete:
            print(' [100%]')
            break
        else:
            print("    %d. retry, resending to: %s" % (i + 1, no_response))

    if no_response:
        print("    no response received in time, even after 3 retries: %s" %
              no_response)
    print("")

    # Having control over your retries is powerful and gives you lots of
    # flexibility, but sometimes you don't want to deal with it manually and
    # just want 'the right thing' to be done for you.
    #
    # Fortunately, MultiPing provides a ready-made function to do the retry for
    # you, called multi_ping(). Specify the overall timeout and the number of
    # additional retries (which are attempted within this timeout). Omit the
    # 'retry' parameter or set to 0 and there will only be a single send.
    #
    # We are also adding an address we won't be able to resolve and set the
    # 'ignore_lookup_errors' flag, to show that those can be ignored if wanted.
    # They will just appear in the 'no response' return list. If the flag is
    # not set then an exception would be thrown.
    addrs.append("cannot.resolve.thiscom")
    print("sending again, waiting with retries via provided send_receive()")
    responses, no_response = multi_ping(addrs, timeout=0.5, retry=2,
                                        ignore_lookup_errors=True)
    print("    reponses: %s" % list(responses.keys()))
    if no_responses:
        print("    no response received in time, even after retries: %s" %
              no_response)
