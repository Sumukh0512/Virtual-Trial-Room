def predict():
  import sys
  import argparse
  opt = argparse.Namespace(name="GMM",
  			   gpu_ids="",
                          workers=4,
                          batch_size=1,
                          dataroot='static/Database',
                          datamode='val',
                          stage='GMM',
                          data_list='val_pairs.txt',
                          fine_width=192,
                          fine_height=256,
                          radius=5,
                          grid_size=5,
                          tensorboard_dir='tensorboard',
                          result_dir='output',
                          checkpoint='checkpoints/GMM/gmm_final.pth',
                          display_count=1,
                          shuffle='')
  from run_gmm import run,GMM,load_checkpoint,CPDataset,CPDataLoader,torch,os,SummaryWriter,torch
  print("Start to test stage: %s, named: %s!" % (opt.stage, opt.name))
  # model.cuda()
  #model.eval()
  test_dataset = CPDataset(opt)
  test_loader = CPDataLoader(opt, test_dataset)
  if not os.path.exists(opt.tensorboard_dir):
        os.makedirs(opt.tensorboard_dir)
  board = SummaryWriter(logdir=os.path.join(opt.tensorboard_dir, opt.name))
  model = GMM(opt)
  datamode='val'
  load_checkpoint(model, opt.checkpoint)
  with torch.no_grad():
            run(opt, test_loader, model, board,datamode)
  print('Successfully completed')
  opt = argparse.Namespace(name='TOM',
  			   gpu_ids='',
                          workers=4,
                          batch_size=1,
                          dataroot='static/Database',
                          datamode='val',
                          stage='TOM',
                          data_list='val_pairs.txt',
                          fine_width=192,
                          fine_height=256,
                          radius=5,
                          grid_size=5,
                          tensorboard_dir='tensorboard',
                          result_dir='output',
                          checkpoint='checkpoints/TOM/tom_final.pth',
                          display_count=1,
                          shuffle='')
  from run_tom import run,UnetGenerator,load_checkpoint,CPDataset,CPDataLoader,torch,os,SummaryWriter,nn,torch
  print("Start to test stage: %s, named: %s!" % (opt.stage, opt.name))
  # model.cuda()
  #model.eval()
  test_dataset = CPDataset(opt)
  test_loader = CPDataLoader(opt, test_dataset)
  if not os.path.exists(opt.tensorboard_dir):
  	    os.makedirs(opt.tensorboard_dir)
  board = SummaryWriter(logdir=os.path.join(opt.tensorboard_dir, opt.name))
  model = UnetGenerator(26, 4, 6, ngf=64, norm_layer=nn.InstanceNorm2d)  # CP-VTON+
  load_checkpoint(model, opt.checkpoint)
  datamode='val'
  with torch.no_grad():
  	    run(opt, test_loader, model, board, datamode)
  print('Successfully completed')
# Resive image code


